import streamlit as st

from ..core import answer
from ..core import question

'''
Administration of question templates.
'''

def template():
    for template in st.session_state.templates.values():
        st.write(template._format)
    # Select template
    def callback():
        # Allow * and / for number questions
        if st.session_state.current_template.__class__ == question.NumberQuestionTemplate:
            st.session_state.settings['乗除を含む問題を生成する'] = True
        selected = st.session_state['template_selectbox']
        st.session_state.current_template = st.session_state.templates[selected]
        st.session_state.current_question = st.session_state.current_template.generate()
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
    st.header('  \n問題形式の追加')
    name_input = st.text_input('問題形式の名前')
    type_selectbox = st.selectbox(label = '問題の種類', options = ['文字式問題', '展開問題', '因数分解問題','整数問題'])
    
    st.write('$' + answer.parse('format_input') + '$')
  
    with st.empty():
        st.session_state.format_keyboard.place()

    if name_input in st.session_state.templates:
        st.error('その名前はすでに使われています')
    
    if st.button('追加'):
        try:
            match type_selectbox:
                case '文字式問題':
                    cls = question.QuestionFormat
                case '展開問題':
                    cls = question.ExpansionQuestionFormat
                case '因数分解問題':
                    cls = question.FactorizationQuestionFormat
                case '整数問題':
                    cls = question.NumberQuestionFormat
                case capture:
                    st.error('内部エラーが発生しました;error during matching question type;  \ninvalid question type passed')
                    st.stop()

            # Check if the given question format is true
            if '＜文字＞' not in st.session_state.format_input and type_selectbox != '整数問題':
                cls = question.NumberQuestionFormat
            elif '＜文字＞' in st.session_state.format_input and type_selectbox == '整数問題':
                cls = question.QuestionFormat
                    
            st.session_state.templates[name_input] = cls(answer.format_evaluate('format_input'))
            
        except SyntaxError:
            st.error('無効な形式です  \nカッコを閉じ忘れたりしていませんか？')

        st.rerun()

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
