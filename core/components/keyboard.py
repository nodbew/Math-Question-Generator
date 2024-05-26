import streamlit as st

from . import inputter

class Keyboard:
    def __init__(self, keys:dict, target:str = "input") -> None:
        """
        Takes a dictionary of key_to_show:input_when_pressed
        Target should be a valid attribute of st.session_state
        """
        if target not in st.session_state:
            raise KeyError(f"st.session_state does not have a key {target}")
        
        buttons = [key : inputter.input(value) for key, value in keys.items()]
        
        def _place():
            