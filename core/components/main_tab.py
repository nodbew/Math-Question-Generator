import streamlit as st
import sympy as sy

from ..core import answer
from . import initialize as init
from .keyboard import Keyboard

'''
Main tab that shows a question and awaits an answer.
'''

def main():
    st.write(st.session_state.current_question)
    if st.session_state.checked:
        # Answer checking(also used for initialization)
        if st.session_state.current_template.check_answer(answer.evaluate("input")):
            st.success('正解!正答は ' + '$' + ", ".join(sy.latex(ans) for ans in st.session_state.current_template.get_answers()) + '$')
            st.session_state.correct_count += 1
        else:
            st.error('不正解...正解は ' + '$' + ", ".join(sy.latex(ans) for ans in st.session_state.current_template.get_answers()) + '$')

        st.session_state.count += 1

        # Generate another question
        try:
            st.session_state.current_question = st.session_state.current_template.generate()
        except answer.RegulationError as e:
            st.error(str(e))
            
        # Initialize input
        st.session_state.input = []
        st.session_state.input_keyboard = Keyboard(
        init.default_keyboard() | {
        c:c for c in st.session_state.current_template._characters.keys()
        }
        )

        st.session_state.checked = False
        
    # Print question and formula
    st.write(st.session_state.current_template.QUESTION)
    st.write('$' + sy.latex(st.session_state.current_question) + '$')
    st.write("$" + answer.parse("input") + "$")
    
    with st.empty():
        st.session_state.input_keyboard.place()

    # Answer button
    if st.button('答える'):
        st.session_state.checked = True

    return
    
