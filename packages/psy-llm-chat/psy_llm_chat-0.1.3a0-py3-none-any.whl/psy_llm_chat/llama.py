from transformers import (
    LlamaForCausalLM,
    LlamaTokenizer,
    AutoTokenizer
    )

import torch
from copy import deepcopy
from typing import List, Dict
from spacy.tokens import Token

# Function to load the main model for text generation
def load_model(model_name, quantization, output_hidden_states=False, output_attentions=False):
    model = LlamaForCausalLM.from_pretrained(
        model_name,
        return_dict=True,
        load_in_8bit=quantization,
        device_map="auto",
        low_cpu_mem_usage=True,
        output_hidden_states=output_hidden_states,
        output_attentions=output_attentions,
    )
    return model


class LlamaChat(object):
    B_INST, E_INST = "<s>[INST]", "[/INST]\n"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"
    STOP = "END_THIS_NOW"
    def __init__(self,
                 model_name,
                 quantization,
                 peft_model: str=None,
                 max_new_tokens: int=256, #The maximum numbers of tokens to generate
                 min_new_tokens: int=0, #The minimum numbers of tokens to generate
                 seed: int=42, #seed value for reproducibility
                 do_sample: bool=True, #Whether or not to use sampling ; use greedy decoding otherwise.
                 use_cache: bool=True,  #[optional] Whether or not the model should use the past last key/values attentions Whether or not the model should use the past last key/values attentions (if applicable to the model) to speed up decoding.
                 top_p: float=1.0, # [optional] If set to float < 1, only the smallest set of most probable tokens with probabilities that add up to top_p or higher are kept for generation.
                 temperature: float=1.0, # [optional] The value used to modulate the next token probabilities.
                 top_k: int=50, # [optional] The number of highest probability vocabulary tokens to keep for top-k-filtering.
                 repetition_penalty: float=1.0, #The parameter for repetition penalty. 1.0 means no penalty.
                 length_penalty: int=1, #[optional] Exponential penalty to the length that is used with beam-based generation.
                 use_fast_kernels: bool = False, # Enable using SDPA from PyTroch Accelerated Transformers, make use Flash Attention and Xformer memory-efficient kernels
                 output_hidden_states: bool = False, #[optional] Enable extraction of hidden states using LlamaChat.extract_hidden_states
                 output_attentions: bool = False, #[optional] Enable extraction of attention layers using LlamaChat.extract_hidden_states
                 silent: bool = False #[optional] Toggle dialog printing
                ):
        self.max_new_tokens = max_new_tokens
        self.min_new_tokens = min_new_tokens
        self.do_sample = do_sample
        self.use_cache = use_cache
        self.top_p = top_p
        self.temperature = temperature
        self.top_k = top_k
        self.repetition_penalty = repetition_penalty
        self.length_penalty = length_penalty
        self.output_hidden_states = output_hidden_states
        self.output_attentions = output_attentions
        self.outputs = []
        self.silent = silent
        
         # Set the seeds for reproducibility
        torch.cuda.manual_seed(seed)
        torch.manual_seed(seed)
        self.model = load_model(model_name, quantization, output_hidden_states = self.output_hidden_states, output_attentions = self.output_attentions)
        if peft_model:
            self.model = load_peft_model(self.model, peft_model)
        if use_fast_kernels:
            """
            Setting 'use_fast_kernels' will enable
            using of Flash Attention or Xformer memory-efficient kernels 
            based on the hardware being used. This would speed up inference when used for batched inputs.
            """
            try:
                from optimum.bettertransformer import BetterTransformer
                self.model = BetterTransformer.transform(self.model)   
            except ImportError:
                print("Module 'optimum' not found. Please install 'optimum' it before proceeding.")

        # self.tokenizer = LlamaTokenizer.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        self.tokenizer.add_special_tokens(
            {
                "pad_token": "<PAD>"
            }
        )
    
    def format_tokens(self, 
                      _dialog: List[Dict],
                      decode: str=None, # decode should be None, or in {`text` | `token_ids` |`all'}
                     ):
        if _dialog[0]["role"] == "system":
            _dialog = [
            {
                "role": _dialog[1]["role"],
                "content": LlamaChat.B_SYS
                + _dialog[0]["content"]
                + LlamaChat.E_SYS
                + _dialog[1]["content"],
            }
        ] + _dialog[2:]
        assert all([msg["role"] == "user" for msg in _dialog[::2]]) and all(
            [msg["role"] == "assistant" for msg in _dialog[1::2]]
        ), (
            "model only supports 'system','user' and 'assistant' roles, "
            "starting with user and alternating (u/a/u/a/u...)"
        )
        """
        Please verify that your tokenizer support adding "[INST]", "[/INST]" to your inputs.
        Here, we are adding it manually.
        """
        dialog_tokens: List[int] = sum(
            [
                self.tokenizer.encode(
                  f"{LlamaChat.B_INST} {(prompt['content']).strip()} {LlamaChat.E_INST} {(answer['content']).strip()} ",
                )
                for prompt, answer in zip(_dialog[::2], _dialog[1::2])
            ],
            [],
        )
        if decode:
            assert decode in ("text","token_ids", "all"), "decode must == (`text` | `token_ids` | `all`)"
            if _dialog[-1]["role"] == "user":
                dialog_tokens += self.tokenizer.encode(
                    f"{LlamaChat.B_INST} {(_dialog[-1]['content']).strip()} {LlamaChat.E_INST}",
                )
            if decode == "text":
                return self.tokenizer.decode(dialog_tokens, skip_special_tokens=True)
            elif decode == "token_ids":
                text = self.tokenizer.decode(dialog_tokens, skip_special_tokens=True)
                print(f"Returning encoding for:\n\n--------------------\n\n{text}\n\n--------------------")
                return dialog_tokens
            else:
                text = self.tokenizer.decode(dialog_tokens, skip_special_tokens=True)
                print(f"Returning encoding for:\n\n--------------------\n\n{text}\n\n--------------------")
                return self.tokenizer(text, return_offsets_mapping=True)
        assert (
            _dialog[-1]["role"] == "user"
        ), f"Last message must be from user, got {_dialog[-1]['role']}"
        dialog_tokens += self.tokenizer.encode(
            f"{LlamaChat.B_INST} {(_dialog[-1]['content']).strip()} {LlamaChat.E_INST}</s>",
        )
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
        assert kind in ["hidden","attention", "both"], f"kind must == ('hidden' | 'attention' | `both`), not {kind}"
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
        encoded = self.tokenizer(self.format_tokens(_dialog, decode="text"), return_tensors="pt")
        output = self.model(input_ids=encoded["input_ids"],attention_mask=encoded["attention_mask"])
        
        # return requested values
        if kind == "hidden":
            result = output.hidden_states
        elif kind == "attention": 
            result = output.attentions
        else:
            result = (output.hidden_states,output.attentions)
        return result
    
    def get_alligned(self,encoding):
        tokens = self.tokenizer.convert_ids_to_tokens(encoding["input_ids"])
        mapping = encoding["offset_mapping"]
        aligned = []
        for token, _map in zip(tokens,mapping):
            if token.startswith("▁") and not _map[0] == 0:
                aligned += [(_map[0]+1,_map[1])]
            else:
                aligned += [_map]
        return aligned

    def get_char_span(self,
                      token):
        start_i = token.idx
        end_i = start_i + len(token.text)
        mapping = (start_i,end_i)
        return mapping
    
    def get_spacy_doc(self,
                      nlp,
                      _dialog: List[Dict],
                      layer: int=-1):
        encoding = self.format_tokens(_dialog, decode = "all")
        text = self.tokenizer.decode(encoding["input_ids"],skip_special_tokens=True)
        embeddings = self.extract_embeddings(_dialog,kind="hidden")[layer].squeeze()
        doc = nlp(text)
        llama_map = self.get_alligned(encoding)
        Token.set_extension("llama_vec", default=None, force=True)
        for token in doc:
            start, stop = self.get_char_span(token)
            slc = tuple(idx for idx, _map in enumerate(llama_map) if _map[0] >= start and _map[1] <= stop and _map[1] != 0)
            token._.llama_vec = embeddings[slc,:].mean(axis=0)
        return doc
    
    def generate(
        self,
        _dialog,
        **kwargs
        ):
        chat = self.format_tokens(_dialog)

        with torch.no_grad():
            tokens= torch.tensor(chat).long()
            tokens= tokens.unsqueeze(0)
            tokens= tokens.to("cuda:0")
            outputs = self.model.generate(
                tokens,
                max_new_tokens=self.max_new_tokens,
                min_new_tokens=self.min_new_tokens,
                do_sample=self.do_sample,
                top_p=self.top_p,
                temperature=self.temperature,
                use_cache=self.use_cache,
                top_k=self.top_k,
                repetition_penalty=self.repetition_penalty,
                length_penalty=self.length_penalty,
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
        last_output = output_text.split(LlamaChat.E_INST)[-1]
        _dialog += [{"role":"assistant","content":last_output}]
        if not self.silent:
            self.print_dialog(_dialog)
        return _dialog
            
    def __call__(self,
                dialog):
        _dialog = deepcopy(dialog)
        if not self.silent:
            self.print_dialog(_dialog)
        inp = False
        outputs = []
        while inp != LlamaChat.STOP:
            output = self.generate(_dialog)
            outputs += [output]
            output_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
            last_output = output_text.split(LlamaChat.E_INST)[-1]
            _dialog += [{"role":"assistant","content":last_output}]
            if not self.silent:
                print(self.dialog_item_to_string(_dialog[-1]))
            inp = input("User: ")
            _dialog += [{"role":"user","content":inp}]
        return _dialog