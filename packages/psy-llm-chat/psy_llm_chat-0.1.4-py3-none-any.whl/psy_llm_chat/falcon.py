from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
from copy import deepcopy
import torch
from typing import List, Dict

# model_id = "tiiuae/falcon-180B"
# model_id = "tiiuae/falcon-180B-chat"

class FalconChat(object):
    STOP = "END_THIS_NOW"
    def __init__(self,
                 model_id,
                 torch_dtype=torch.bfloat16,
                 load_in_8bit=True,
                 load_in_4bit=False,
                 device_map="auto",
                 output_hidden_states=True,
                 output_attentions=False,
                 do_sample=True,
                 temperature=0.6,
                 top_p=0.9,
                 max_new_tokens=500,
                 repetition_penalty: float=1.0, #The parameter for repetition penalty. 1.0 means no penalty.
                 length_penalty: int=1, #[optional] Exponential penalty to the length that is used with beam-based generation.
                 ):
        assert  not (load_in_4bit == True and load_in_8bit == True), "Choose one of `load_in_4bit` or `load_in_8bit`"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = self.load_model(model_id,
                                     torch_dtype, 
                                     load_in_8bit,
                                     load_in_4bit,
                                     device_map,
                                     output_hidden_states,
                                     output_attentions)
        self.do_sample=do_sample #True,
        self.temperature=temperature #0.6,
        self.top_p=top_p #0.9,
        self.max_new_tokens=max_new_tokens #500
        self.repetition_penalty = repetition_penalty
        self.length_penalty = length_penalty
        self.outputs = []
 
    @staticmethod
    def load_model(model_id,
                   torch_dtype,
                   load_in_8bit,
                   load_in_4bit,
                   device_map,
                   output_hidden_states,
                   output_attentions):
        return AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch_dtype,
            load_in_8bit=load_in_8bit,
            load_in_4bit=load_in_4bit,
            device_map=device_map,
            output_hidden_states=output_hidden_states,
            output_attentions=output_attentions)
    
    @staticmethod
    def format_dialog(dialog: List[Dict],
                 ):
        _dialog = deepcopy(dialog)
        system = False
        if _dialog[0]["role"] == "system":
            system_prompt = _dialog.pop(0)
            system_prompt = f"System: {system_prompt['content']}\n"
            system = True
            
        if _dialog[-1]["role"] == "user":
            _dialog += [{"role": "assistant", "content": ""}]

        assert all([msg["role"] == "user" for msg in _dialog[::2]]) and \
            all([msg["role"] == "assistant" for msg in _dialog[1::2]]), \
                ("model only supports 'system','user' and 'assistant' roles, "
                 "starting with user and alternating (u/a/u/a/u...)")

        formatted_dialog = "\n".join([f"User: {(prompt['content']).strip()}\nFalcon: {(answer['content']).strip()}" \
                                      for prompt, answer in zip(_dialog[::2], _dialog[1::2])])
        if system:
            formatted_dialog = f"{system_prompt}{formatted_dialog}"
        return formatted_dialog
    
    @staticmethod
    def print_dialog_item(dialog_item):
        _map  = {"user": "User", "assistant": "Falcon", "system": "System"}
        print(f"{_map[dialog_item['role']]}: {dialog_item['content']}")
        
    def get_last_output(self,output):
        self.outputs += [output]
        return output.split('\nFalcon:')[-1]
        
    def print_dialog(self,
                     dialog):
        for item in dialog:
            self.print_dialog_item(item)
    
    def tokenize(self,
                 formatted_dialog: str):
        return self.tokenizer(formatted_dialog, return_tensors="pt").to("cuda")
    
    def generate(self,
                 inputs):
        with torch.no_grad():
            output = self.model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                do_sample=self.do_sample,
                eos_token_id=193,
                temperature=self.temperature,
                top_p=self.top_p,
                max_new_tokens=self.max_new_tokens#,
                #length_penalty=self.length_penalty,
                #repetition_penalty=self.repetition_penalty                
                )
        output = output[0].to("cpu")
        formatted_output = self.tokenizer.decode(output)
        return formatted_output
    
    def get_response(self,
                     dialog):
        _dialog = deepcopy(dialog)
        assert dialog[-1]["role"] == "user", "Dialog must end with content from the user, i.e. `dialog[-1]['role'] must == 'user'"
        formatted_dialog = self.format_dialog(dialog)
        inputs = self.tokenize(formatted_dialog)
        output = self.generate(inputs)
        _dialog += [{"role":"assistant","content":self.get_last_output(output)}]
        return _dialog
            
    def __call__(self,
                 dialog):
        _dialog = deepcopy(dialog)
        self.print_dialog(_dialog)
        formatted_dialog = self.format_dialog(dialog)
        inp = False
        while inp != FalconChat.STOP:
            _dialog = self.get_response(_dialog)
            self.print_dialog_item(_dialog[-1])
            inp = input("User: ")
            _dialog += [{"role":"user","content":inp}]
        _dialog.pop(-1)
        return _dialog