import streamlit as st

from ..core import generators
from ..data import signs

class ArgumentRecorder(str, int):
    def __init__(self):
        self.__value = 0
        return 

    def __imul__(self, mul:str|int):
        if isinstance(mul, str):
            
        else:
            self.__value *= mul

def _input(input:str|int, target:str) -> None:
    '''
    Adds the input to st.session_state[target](Assigned in core.components.keyboard.Keyboard.__init__, when creating st.button)
    Numbers will be automatically concatenated.
    '''
    if isinstance(input, int):
        if isinstance(st.session_state[target][-2], int):
            st.session_state[target][-2] *= 10
            st.session_state[target][-2] += input
            return
        else:
            st.session_state[target].extend(['{', input, '}'])
            return

    elif input in signs.FUNCTIONS:
        st.session_state[target].extend(['*', input, '{', 0, '}'])
