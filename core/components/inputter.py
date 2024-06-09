import numpy as np
import streamlit as st

from ..core import generators
from ..data import signs

def _input(input:str|int, target:str) -> None:
    '''
    Adds the input to st.session_state.*(Assigned in core.components.keyboard.Keyboard.__init__, when creating st.button)
    Numbers will be automatically concatenated.
    '''
    if input == '＜文字＞':
        next = st.session_state.format_input_CharacterGenerator.__next__()
        st.session_state.format_keyboard.add_key({next:next})
        input = next
        
    elif isinstance(input, generators.NumberGenerator):
        st.session_state[target].append('{')
        st.session_state[target].append(input)
        st.session_state[target].append('}')
        return
        
    elif isinstance(input, generators.OperatorGenerator):
        st.session_state[target].append(input)
        return

    elif isinstance(input, generators.SympyFunction):
        st.session_state[target].append(input)
        st.session_state[target].append('(')
        return
        
    elif input in signs.BRACKETS:
        st.session_state[target].append(input)
        return
    
    if isinstance(input, int):
        try:
            if isinstance(st.session_state[target][-1], int):
                st.session_state[target][-1] *= 10
                st.session_state[target][-1] += input # 1,0 -> 10
                
            else:
                # New number sequence
                if st.session_state[target][-1] not in ('.', '{'):
                    st.session_state[target].append('{')    
                
                if st.session_state[target][-1] not in signs.OPERANDS_AND_FUNCTIONS:
                    st.session_state[target].append('*')    
                    
                st.session_state[target].append(input)
                return
                
        except IndexError:
            st.session_state[target].append("{")
            st.session_state[target].append(input)
            return
    
    else:
        try:
            if isinstance(st.session_state[target][-1], int):
                st.session_state[target].append('}')
                st.session_state[target].append('*')   
                
            st.session_state[target].append(input)
            return
            
        except IndexError:
            st.session_state[target].append(input)
        finally:
            st.session_state[target].append('{')
            return

def callback(input:str, target:str):
    '''
    Takes an input and returns a callback function that appends the input to st.session_state.*
    '''
    match input:
    
        case 'All Clear':
            def _callback():
                st.session_state[target] = []
                return
            return _callback
            
        case 'Back Space':
            def _callback():
                try:
                    st.session_state[target].pop(-1)
                except IndexError:
                    pass
                return
            return _callback
            
        case capture:
            def _callback():
                _input(input, target)
                return
            return _callback
