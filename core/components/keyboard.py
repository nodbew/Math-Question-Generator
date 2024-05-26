import streamlit as st

from . import inputter

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
        if target not in st.session_state:
            raise KeyError(f"st.session_state does not have a key {target}")
        
        buttons = {st.button(
            label = key,
            key = f'Key_{key}_at_keyboard_{id(self)}',
            on_click = inputter.input(value),
            use_container_width = True
                            ) for key, value in keys.items()}
        
        def _place():
            '''
            A function that places the actual keyboard.
            '''
            for i, col in enumerate(st.columns(col_num)):
                buttons_to_use = buttons[i * col_num : (i + 1) * col_num]
                with col:
                    for i in buttons_to_use:
                        if i:pass
            return 
        self._place = _place
        return

    def place(self):
        '''
        Places the keyboard.
        '''
        self._place()
        return
