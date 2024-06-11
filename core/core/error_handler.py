from functools import wraps

import streamlit as st
import sympy as sy

def error_handler(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
            
        except Exception as e:
            err_msg = f'エラーが起きました：{str(e)}  \n種別：{e.__class__}'
            st.error(err_msg)
            return sy.nan
        return

    return _wrapper
