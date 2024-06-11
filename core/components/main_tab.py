import streamlit as st
import sympy as sy

from ..core import answer

'''
Main tab that shows a question and awaits an answer.
'''

def main():
    
    # Print question and formula
    st.write(st.session_state.current_template.QUESTION)
    st.write('$' + answer.parse(False, sy.latex(st.session_state.current_question)) + '$')

    if st.session_state.checked:
        # Answer checking(also used for initialization)
        st.write('正解は ' + '$' + ", ".join(sy.latex(ans) for ans in st.session_state.current_template.get_answers()) + '$')

        st.session_state.count += 1

        # Generate another question
        try:
            st.session_state.current_question = st.session_state.current_template.generate()
        except answer.RegulationError as e:
            st.error(str(e))

        st.session_state.checked = False

        if st.button('次へ'):
            st.rerun()

    else:

        # Answer button
        if st.button('答える'):
            st.session_state.checked = True

    return
    
