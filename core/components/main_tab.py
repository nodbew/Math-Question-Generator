import streamlit as st
import sympy as sy

from ..core import answer

'''
Main tab that shows a question and awaits an answer.
'''

def main():
    # Answer checking(also used for initialization)
    if st.session_state.checked:
        # Set checked to False
        st.session_state.checked = False

        # Check answer
        result = st.session_state.current_template.check_answer(
            answer.evaluate()
        )
        if result:
            st.success('正解！')
            st.session_state.correct_count += 1
        elif result == False:
            st.error('不正解...  \n正解は ' + '$' + ", ".join(sy.latex(ans) for ans in st.session_state.current_template._answer) + '$')
        elif result is None:
            pass

        st.session_state.count += 1

        # Generate another question
        st.session_state.current_question = st.session_state.current_template.generate()

        # Initialize user input
        st.session_state.input = []

    # Print question and formula
    st.write(st.session_state.current_template.QUESTION)
    st.write('$' + st.session_state.current_question + '$')

    # Print user input
    st.write("$" + answer.parse() + "$")

    # Place keyboard
    with st.empty():
        st.session_state.input_keyboard.place()

    # Answer button
    if st.button('答える'):
        st.session_state._checked = True

    return
    
