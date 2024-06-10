import streamlit as st
import datetime

'''
Show statistics.
'''

def statistics():
    st.write('累計回答数：' + str(st.session_state.count))
    st.write('累計正解数：' + str(st.session_state.correct_count))
    st.write('正答率：' + str(st.session_state.correct_count // st.session_state.count * 10))
    st.write('累計時間：' + str(datetime.datetime.now() - st.session_state.start_time))
    if st.button("更新"):pass # for rerunning 
    return 
