import streamlit as st

import core.core.initialize as init
import core.components.initialize as comp_init

if 'settings' not in st.session_state:
    st.session_state.settings = init.settings()
if 'OperandGenerator' not in st.session_state:
    st.session_state.OperandGenerator = init.operand_generator()
if 'input' not in st.session_state:
    st.session_state.input = []
if 'input_for_format' not in st.session_state:
    st.session_state.input_for_format = []
if 'input_keyboard' not in st.session_state:
    st.session_state.input_keyboard = comp_init.default_keyboard()
if 'format_input_keyboard' not in st.session_state:
    st.session_state.format_input_keybaord = comp_init.default_format_keyboard()
