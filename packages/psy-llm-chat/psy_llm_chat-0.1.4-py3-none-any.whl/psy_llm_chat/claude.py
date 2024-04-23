import time
import json
from copy import deepcopy

class ClaudeChat(object):
    STOP = "END_THIS_NOW"
    def __init__(self,
                 client,
                 model="claude-3-opus-20240229",
                 temperature=0.6,
                 max_tokens=1000,
                 sleep=300,
                 silent=False,
                 system = None):
        self.client = client
        self.model = model
        self.temperature=temperature
        self.max_tokens=max_tokens
        self.sleep = sleep
        self.silent = silent
        self.system = system
    
    def _call_api(self,
                 _dialog):
        if self.system:
            return self.client.messages.create(
                model=self.model,
                messages=_dialog,
                system=self.system,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
        return self.client.messages.create(
            model=self.model,
            messages=_dialog,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
    
    def _error_wrapper(self,
                  _dialog):
        try:
            response = self._call_api(_dialog)
        except Exception as e:
            print(f"An exception occurred: {e}")
            time.sleep(self.sleep)
            response = self._call_api(_dialog)
        return response
    
    def _print_dialog(self,_dialog):
        if self.model.startswith("claude"):
            for m in _dialog:
                print(f"{list(m.values())[0].capitalize()}: {list(m.values())[1]}")
                    
    def _slicer(self,res, kind):
        if self.model.startswith("claude"):
            if kind == "role":
                return res.role
            elif kind == "content":
                return res.content[0].text
                
    def get_response(self,
                     dialog):
        _dialog = deepcopy(dialog)
        res = self._error_wrapper(_dialog)
        content = self._slicer(res,"content")
        role = self._slicer(res,"role")
        _dialog += [{"role":role,"content":content}]
        if not self.silent:
            self._print_dialog(_dialog)
        return _dialog

    def run_chat(self,
                 dialog):
        _dialog = deepcopy(dialog)
        self._print_dialog(_dialog)
        while _dialog[-1]["content"] != ClaudeChat.STOP:
            res = self._error_wrapper(_dialog)
            content = self._slicer(res,"content")
            role = self._slicer(res, "role")
            _dialog += [{"role":role,"content":content}]
            print(f"{role.capitalize()}: {content}")
            user_input = input("User: ")
            _dialog += [{"role":"user","content":user_input}]
        return _dialog
            
    def __call__(self,dialog):
        return self.run_chat(dialog)