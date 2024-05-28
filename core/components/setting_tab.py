import streamlit as st

'''
Modify settings about problem generation and answer interpreting.
'''

def change_setting(name):
    st.session_state.settings[name] = not st.session_state.settings[name]

def setting():
    st.header('問題生成に関する設定を変更できます')

    # Create checkboxes 
    for name, value in st.session_state.settings.items():
        st.checkbox(name, 
                    value = value, 
                    key = 'setting_checkbox_' + name,
                    on_change = change_setting,
                    args = (name,)')
                   )
    return
