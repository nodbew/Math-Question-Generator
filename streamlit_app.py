import streamlit as st

import core.initialize as init

if 'settings' not in st.session_state:
    st.session_state.settings = init.settings()
if 'OperandGenerator' not in st.session_state:
    st.session_state.OperandGenerator = init.operand_generator()
if 'input' not in st.session_state:
    st.session_state.input = []
if 'input_for_format' not in st.session_state:
    st.session_state.input_for_format = []
