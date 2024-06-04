import streamlit as st

from ..core import answer

'''
Administration of question templates.
'''

def template():
    # Select template
    def callback():
        selected = st.session_state['template_selectbox']
        st.session_state.current_template = st.session_state.templates[selected]
        st.session_state.current_question = st.session_state.current_template.generate()
        st.rerun()
        return
        
    st.header('問題形式の選択')
    options = list(st.session_state.templates.keys())
    template = st.selectbox(
        label = '問題形式',
        key = 'template_selectbox',
        options = options,
        index = options.index('二次方程式の求解'),
        on_change = callback
    )

    # Add template
    st.header('問題形式の追加')
    st.write('$' + answer.parse('format_input') + '$')
  
    with st.empty():
        st.session_state.format_keyboard.place()

    name_input = st.text_input('問題形式の名前')
    type_selectbox = st.selectbox(label = '問題の種類', options = ['普通の問題', '展開問題', '因数分解問題'])
    
    if st.button('追加'):
        try:
            match type_selectbox:
                case '普通の問題':
                    cls = question.QuestionTemplate
                case '展開問題':
                    cls = question.ExpansionQuestionTemplate
                case '因数分解問題':
                    cls = question.FactorizationQuestionTemplate
                case capture:
                    st.error('内部エラーが発生しました;error during matching question type:invalid question type passed')
                    st.stop()
                    
            st.session_state.templates[name] = cls(answer.format_evaluate('format_input'))
            
        except SyntaxError:
            st.error('無効な形式です  \nカッコを閉じ忘れたりしていませんか？')

    # Delete template
    st.header('問題形式の削除')
    st.info('現在選択されている問題形式を削除します')
    if st.button('削除'):
        for key, value in st.session_state.templates.items():
            if value is st.session_state.current_template:
                del st.session_state.templates[key]
                break
                
        del st.session_state.current_template
        st.session_state.current_template = st.session_state.templates[0]
    
    return
