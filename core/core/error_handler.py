from functools import wraps

import streamlit as st
'''
def error_handler(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
            
        except Exception as e:
            err_msg = f'エラーが起きました：{str(e)}  \n種別：{e.__class__}'
            st.error(err_msg)
        return

    return _wrapper
'''
def error_handler(func):
    # Nothing is implemented for debugging
    def _wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return _wrapper
