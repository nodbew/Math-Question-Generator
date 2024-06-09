import streamlit as st

from ..core import generators
from ..data import signs

def input(input:str|int, target:str) -> None:
    '''
    Adds the input to st.session_state[target](Assigned in core.components.keyboard.Keyboard.__init__, when creating st.button)
    Numbers will be automatically concatenated.
    '''
    # If this is the first input
    if len(st.session_state[target]) == 0:
        if isinstance(input, int):
            st.session_state[target].extend(['{', input])
            return
            
        elif input == r'\Character':
            next = st.session_state.format_input_CharacterGenerator.__next__()
            st.session_state.format_keyboard.add_keys({next:next}, target = 'format_input')
            st.session_state[target].extend(['{', input, '}'])
            pass # Input will be changed to an alphabet, but the function does not end its process instantly
        
        elif isinstance(input, generators.NumberGenerator):
            st.session_state[target].extend(['{', input, '}'])
            return

        if input in signs.BRACKETS:
            st.session_state[target].append(input)
            return

        # Other special cases
        if input in signs.CALCULATION_SIGNS or isinstance(input, generators.OperatorGenerator):
            st.session_state[target].append(input)
            return

        elif input in signs.FUNCTIONS:
            st.session_state[target].extend([input, '{', 0]) # There will be a number or a constant 
            return
    
        # Other cases (constants, characters)
        else:
            st.session_state[target].extend(['{', input])

    # The input is a number
    if isinstance(input, int):
        # 1, 0 -> 10 (= 1*10 + 0)
        if isinstance(st.session_state[target][-1], int):
            st.session_state[target][-1] *= 10
            st.session_state[target][-1] += input

        elif st.session_state[target][-1] in (signs.OPERATORS + ('{',)) or isinstance(st.session_state[target][-1], generators.OperatorGenerator):
            st.session_state[target].extend(['{', input])

        # sin, (, 2π, ), 20 -> sin(2π)*{20
        else:
            st.session_state[target].extend(['*', '{', input])
            
        return

    # Special inputs for creating format
    if input == r'\Character':
        next = st.session_state.format_input_CharacterGenerator.__next__()
        st.session_state.format_keyboard.add_keys({next:next}, target = 'format_input')
        input = next
        pass # Input will be changed to an alphabet, but the function does not end its process instantly
        
    elif isinstance(input, generators.NumberGenerator):
        if st.session_state[target][-1] in (signs.OPERATORS + ('{',)) or isinstance(st.session_state[target][-1], generators.OperatorGenerator):
            st.session_state[target].extend(['{', input, '}'])

        # sin, (, 2π, ), 20 -> sin(2π)*{20
        else:
            st.session_state[target].extend(['*', '{', input, '}'])
        return

    # Special inputs for both format and normal input
    if input in signs.BRACKETS:
        st.session_state[target].append(input)
        return

    # Other special cases
    if input in signs.CALCULATION_SIGNS or isinstance(input, generators.OperatorGenerator):
        if isinstance(st.session_state[target][-1], int):
            st.session_state[target].append('}')

        st.session_state[target].append(input)
        return

    elif input in signs.FUNCTIONS:
        st.session_state[target].extend([input, '{', 0]) # There will be a number or a constant 
        return

    # Other cases (constants, characters)
    else:
        st.write('ur partly right')
        if st.session_state[target][-1] == 0:
            # See 'elif input in signs.FUNCTIONS' clause
            # FUNCTION{, a should not be converted into FUNCTION{ (0 * a)
            st.session_state[target].pop(-1)
            st.session_state[target].extend(['{', input])
            return
            
        elif isinstance(st.session_state[target][-1], int) or st.session_state[target][-1] in signs.CONSTANTS:
            st.session_state[target].extend(['}', '*', '{', input])
            return

        elif st.session_state[target][-1] == '}':
            st.session_state[target].extend(['*', '{', input])

        else:
            st.write('ur right')
            st.session_state[target].extend(['{', input])
            return
