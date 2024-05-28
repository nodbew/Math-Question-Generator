import streamlit as st

from ..core import answer

'''
Administration of question templates.
'''

def template():
    # Select template
    st.header('問題形式の選択')
    options = list(st.session_state.templates.keys())
    st.selectbox(
        label = '問題形式',
        key = 'template_selectbox',
        options = options,
        index = options.index('二次方程式の求解'),
        on_change = exec('st.session_state.apis["change_current_template"](key = "template_selectbox")')
    )

    # Add template
    st.header('問題形式の追加')
    st.write('$' + 
             answer.parse('format_input') + 
             '$')
  
    with st.empty():
        st.session_state.format_keyboard.place()
    type_selectbox = st.selectbox(label = '問題の種類', options = ['普通の問題', '展開問題', '因数分解問題')
    if st.button('追加'):
        try:
            st.session_state.templates.append(eval(type_selectbox)(answer.parse('format_input')))
        except SyntaxError:
            st.error('無効な形式です  \nカッコを閉じ忘れたりしていませんか？')

    # Delete template
    st.header('問題形式の削除')
    st.info('現在選択されている問題形式を削除します')
    if st.button('削除'):
        st.session_state.templates.pop(st.session_state.templates.index(st.session_state.current_template))
        del st.session_state.current_template
        st.session_state.current_template = st.session_state.templates[0]
    
    return
