def _input(input:str|int, target:str) -> None:
    '''
    Adds the input to st.session_state[target](Assigned in core.components.keyboard.Keyboard.__init__, when creating st.button)
    Numbers will be automatically concatenated.
    '''

    # The input is a number
    if isinstance(input, int):
        # 1, 0 -> 10 (= 1*10 + 0)
        if isinstance(st.session_state[target][-1], int):
            st.session_state[target][-1] *= 10
            st.session_state[target][-1] += input

        # sin, (, 2π, ), 20 -> sin(2π)*{20
        else:
            st.session_state[target].append('*')
            st.session_state[target].append('{')
            st.session_state[target].append(input)

        return

    # Special inputs for creating format
    if input == r'\Character':
        next = st.session_state.format_input_CharacterGenerator.__next__()
        st.session_state.format_keyboard.add_keys({next:next}, target = 'format_input')
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

    # Special inputs for both format and normal input
    if input in signs.BRACKETS:
        st.session_state[target].append(input)
        return

    elif input in signs.FUNCTIONS:
        st.session_state[target].append(input)
