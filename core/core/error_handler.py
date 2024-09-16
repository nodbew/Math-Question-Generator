from functools import wraps

import streamlit as st
import sympy as sy

def error_handler(func):
    """
    Captures any error and prints the error's type to the console
    """
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
            
        except Exception as e:
            st.error(f'エラーが起きました：{e}  \n種別：{e.__class__}')
            return None

    return _wrapper
