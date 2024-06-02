import streamlit as st
import sympy as sy

from ..core import answer

'''
Main tab that shows a question and awaits an answer.
'''

def main():
    
    # Print question and formula
    st.write(st.session_state.current_template.QUESTION)
    st.write('$' + sy.latex(st.session_state.current_question) + '$')

    if st.session_state.checked:
        # Answer checking(also used for initialization)
        st.write('正解は ' + '$' + ", ".join(sy.latex(ans) for ans in st.session_state.current_template._answer) + '$')

        st.session_state.count += 1

        # Generate another question
        st.session_state.current_question = st.session_state.current_template.generate()

        if st.button('次へ'):
            st.session_state.checked = False

    else:

        # Answer button
        if st.button('答える'):
            st.session_state.checked = True

    return
    
