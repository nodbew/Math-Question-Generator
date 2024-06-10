import streamlit as st

from ..core import generators
from ..data import signs

def _input(input:str|int, target:str) -> None:
    st.write('input function called')
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

        elif st.session_state[target][-1] in (signs.CALCULATION_SIGNS + ('{',)) or isinstance(st.session_state[target][-1], generators.OperatorGenerator):
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
        if st.session_state[target][-1] in (signs.CALCULATION_SIGNS + ('{',)) or isinstance(st.session_state[target][-1], generators.OperatorGenerator):
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
        if st.session_state[target][-1] == 0:
            st.session_state[target].pop(-1)
            st.session_state[target].append(input)
            return

        elif st.session_state[target][-1] not in (signs.CALCULATION_SIGNS + signs.BRACKETS):
            st.session_state[target].append('}')

        st.session_state[target].append(input)
        return

    elif input in signs.FUNCTIONS:
        if st.session_state[target] == 0:
            st.session_state[target].pop(-1)
            st.session_state[target].extend([input, '{', 0])
            return

        elif st.session_state[target][-1] in (signs.CALCULATION_SIGNS + signs.BRACKETS):
            st.session_state[target].extend(['*', input, '{', 0])

        else:
            st.session_state[target].extend(['}', '*', input, '{', 0]) # There will be a number or a constant 
        return

    # Other cases (constants, characters)
    else:
        if st.session_state[target][-1] == 0:
            # See 'elif input in signs.FUNCTIONS' clause
            # FUNCTION{, a should not be converted into FUNCTION{ (0 * a)
            st.session_state[target].pop(-1)
            st.session_state[target].extend(['{', input])
            return

        elif st.session_state[target][-1] == '}':
            st.session_state[target].extend(['*', '{', input])

        else:
            st.session_state[target].extend(['}', '*', '{', input])
            return

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
