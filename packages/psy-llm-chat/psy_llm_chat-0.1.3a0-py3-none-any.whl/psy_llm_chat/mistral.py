from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer
    )

import torch
from copy import deepcopy
from typing import List, Dict

# Function to load the main model for text generation
def load_model(model_name, quantization, output_hidden_states=False, output_attentions=False):
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        load_in_8bit=quantization,
        device_map="auto",
        low_cpu_mem_usage=True,
        output_hidden_states=output_hidden_states,
        output_attentions=output_attentions,
    )
    return model

class MistralChat(object):
    B_INST, E_INST = "[INST]", "[/INST]"
    STOP = "END_THIS_NOW"
    def __init__(self,
                 model_name,
                 quantization,
                 seed=42,
                 temperature=1,
                 do_sample=True,
                 device="cuda",
                 max_new_tokens: int=256, #The maximum numbers of tokens to generate
                 min_new_tokens: int=0, #The minimum numbers of tokens to generate
                 output_hidden_states: bool = False, #[optional] Enable extraction of hidden states using LlamaChat.extract_hidden_states
                 output_attentions: bool = False, #[optional] Enable extraction of attention layers using LlamaChat.extract_hidden_states
                 silent: bool = False #[optional] Toggle dialog printing
                ):
        self.seed=seed,
        self.temperature = temperature
        self.do_sample = do_sample
        self.device=device
        self.max_new_tokens = max_new_tokens
        self.min_new_tokens = min_new_tokens
        self.output_hidden_states = output_hidden_states
        self.output_attentions = output_attentions
        self.outputs = []
        self.silent = silent
        # Set the seeds for reproducibility
        torch.cuda.manual_seed(seed)
        torch.manual_seed(seed)
        # Load model + Tokenizer
        self.model = load_model(model_name, quantization, output_hidden_states = self.output_hidden_states, output_attentions = self.output_attentions)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
       
    def format_tokens(self, 
                      _dialog: List[Dict],
                      decode: str=None, # decode should be None, or in {`text` | `token_ids` |`all'}
                     ):
        if decode:
            assert decode in ("text","token_ids", "all"), "decode must == (`text` | `token_ids` | `all`)"
            if decode == "text":
                return tokenizer.decode(tokenizer.apply_chat_template(_dialog))
            elif decode == "token_ids":
                dialog_tokens = self.tokenizer.apply_chat_template(_dialog, return_tensors="pt")
                return dialog_tokens
            else:
                text = tokenizer.decode(tokenizer.apply_chat_template(_dialog))
                return self.tokenizer(text, return_offsets_mapping=True, return_tensors="pt")
        else:
            dialog_tokens = self.tokenizer.apply_chat_template(_dialog, return_tensors="pt")
        return dialog_tokens
    
    def dialog_item_to_string(self,
                       dialog_item):
        return f"{dialog_item['role'].capitalize()}: {dialog_item['content']}"
    
    def print_dialog(self,
                     _dialog):
        for dialog_item in _dialog:
            print(self.dialog_item_to_string(dialog_item))
    
    def extract_embeddings(self,
                           _dialog,
                           kind="hidden"):
        assert kind in ["hidden","attention", "logits", "past_key_values", "both"], f"kind must == ('hidden' | 'attention' | | `logits` | `past_key_values` | `both`), not {kind}"
        if kind == "hidden":
            assert self.model.config.output_hidden_states, f"model.config.output_hidden_states must be `True` not `{self.model.config.output_hidden_states}`"
        elif kind == "attention":
            assert self.model.config.output_attentions, f"model.config.output_attentions must be `True` not `{self.model.config.output_attentions}`"
        else: 
            assert (
                self.model.config.output_hidden_states and self.model.config.output_attentions
            ), (
                f"model.config.output_hidden_states must be `True` not `{self.model.config.output_hidden_states}`",
                f"model.config.output_attentions must be `True` not `{self.model.config.output_attentions}`"
                )
        # get text string of dialog 
        encoded = self.format_tokens(_dialog, decode="all")
        output = self.model(input_ids=encoded["input_ids"],attention_mask=encoded["attention_mask"])

        # return requested values
        if kind == "hidden":
            result = output.hidden_states
        elif kind == "attention": 
            result = output.attentions
        elif kind == "logits":
            result = output.logits
        elif kind == "past_key_values":
            result = output.past_key_values
        else:
            result = output
        return result
    
    def generate(
        self,
        _dialog,
        **kwargs
        ):
        chat = self.format_tokens(_dialog)
        
        with torch.no_grad():
            #send to device
            tokens = chat.to(self.device)
            outputs = self.model.generate(
                tokens,
                max_new_tokens=self.max_new_tokens,
                min_new_tokens=self.min_new_tokens,
                do_sample=self.do_sample,
                temperature=self.temperature,
                pad_token_id=self.tokenizer.eos_token_id,
                **kwargs
            )
        return outputs
    
    
    def get_response(self,
                     dialog):
        _dialog = deepcopy(dialog)
        output = self.generate(_dialog)
        self.outputs += [output]
        output_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        last_output = output_text.split(MistralChat.E_INST)[-1].strip()
        _dialog += [{"role":"assistant","content":last_output}]
        if not self.silent:
            self.print_dialog(_dialog)
        return _dialog
        
    def __call__(
        self,
        dialog
    ):
        _dialog = deepcopy(dialog)
        if not self.silent:
            self.print_dialog(_dialog)
        inp = False
        outputs = []
        while inp != MistralChat.STOP:
            output = self.generate(_dialog)
            outputs += [output]
            output_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
            last_output = output_text.split(MistralChat.E_INST)[-1]
            _dialog += [{"role":"assistant","content":last_output}]
            if not self.silent:
                print(self.dialog_item_to_string(_dialog[-1]))
            inp = input("User: ")
            _dialog += [{"role":"user","content":inp}]
        return _dialog