import streamlit as st

from . import inputter

class ButtonPlaceHolder:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        return

    def __getattr__(self, attr, default = None):
        if attr in self._kwargs:
            return self._kwargs[attr]
        else:
            return default
        
    def __bool__(self):
        return st.button(*args, **kwargs)

class Keyboard:
    '''
    Prepares a virtual keyboard with the given keys.
    Places it when "place" method is called.
    '''
    def __init__(self, keys:dict, target:str = "input", col_num:int = 7) -> None:
        """
        Takes a dictionary of key_to_show:input_when_pressed
        Target should be a valid attribute of st.session_state
        """
        self._col_num = col_num
        
        self._buttons = [ButtonPlaceHolder(
            label = key,
            key = f'Key_{key}_at_keyboard_{id(self)}',
            on_click = inputter.callback(value, target),
            use_container_width = True
                            ) for key, value in keys.items()]
        return
    
    def add_keys(self, keys:dict):
        '''
        Adds the given keys to the keyboard.
        '''
        new_buttons = [st.button(
            label = key,
            key = f'key_{key}_at_keyboard_{id(self)}',
            on_click = inputter.callback(value, target),
            use_container_width = True,
        ) for key, value in keys.items()]
        
        self._buttons += new_buttons
        return

    def remove_keys(self, key:str|list):
        if type(key) == str:
            self._buttons = [btn for btn in self._buttons if not (btn.key == f'key_{key}_at_keyboard_{id(self)}')]
            return
        elif type(key) == list:
            for key in keys:
                self.remove_key(key)
            return
        else:
            raise TypeError(f'An argument for Keyboard.remove_key method must be a str of a list, not {type(key)}')

    def get_keys(self):
        return [btn.key for btn in self._buttons]

    def place(self):
        '''
        Places the keyboard.
        '''
        col_num = self._col_num
        
        for i, col in enumerate(st.columns(col_num)):
            buttons_to_use = self._buttons[i * col_num : (i + 1) * col_num]
            with col:
                for i in buttons_to_use:
                    if i:
                        pass
        return
