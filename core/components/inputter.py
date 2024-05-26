def _input(input:str) -> str|int:
    '''
    Adds the input to st.session_state.*(Assigned in core.components.keyboard.Keyboard.__init__, when creating st.button)
    '''
    return input

def input(input:str, target:str):
    '''
    Takes an input and returns a callback function that appends the input to st.session_state.*
    '''
    if input == 'All Clear':
        def _callback():
            st.session_state[target] = []
            return
        return _callback
    elif input == 'Back Space':
        def _callback():
            st.session_state.pop(-1)
            return
        return _callback
    else:
        def _callback():
            return _input(input)
        return _callback
