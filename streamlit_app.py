import streamlit as st
import sympy as sy
import datetime

import core.core.initialize as init
import core.components.initialize as comp_init
import core.core.question as question
import core.core.generators as generators
from core.components.keyboard import Keyboard

# Initialization of st.session_state
if 'settings' not in st.session_state:
    st.session_state.settings = init.settings()
if 'OperandGenerator' not in st.session_state:
    st.session_state.OperatorGenerator = init.operator_generator()
if 'format_input' not in st.session_state:
    st.session_state.format_input = []
if 'format_keyboard' not in st.session_state:
    st.session_state.format_keyboard = Keyboard(comp_init.default_format_keyboard(), target = 'format_input')
if 'settings' not in st.session_state:
    st.session_state.settings = init.settings()

if 'templates' not in st.session_state:
    st.session_state.templates = {
        '二次方程式の求解' : init.polynomial_problem(),
        '二次方程式の展開' : question.ExpansionQuestionFormat(init.polynomial_problem(raw_format = True)),
        '二次方程式の因数分解' : question.FactorizationQuestionFormat(init.polynomial_problem(raw_format = True)),
        '整数問題' : question.NumberQuestionFormat([generators.NumberGenerator(), st.session_state.OperandGenerator, generators.NumberGenerator()])
    }
    
if 'current_template' not in st.session_state:
    st.session_state.current_template = st.session_state.templates['二次方程式の求解']
if 'current_question' not in st.session_state:
    st.session_state.current_question = st.session_state.current_template.generate()
if 'checked' not in st.session_state:
    st.session_state.checked = False
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.datetime.now()

# Tabs
import core.components.main_tab as main
import core.components.setting_tab as setting
import core.components.template_tab as template
import core.components.statistics_tab as statistics

# Create tab objects with names
main_tab, template_tab, setting_tab, statistics_tab = st.tabs(['出題', '問題形式', '設定', '統計'])

with main_tab:
    main.main()
with template_tab:
    template.template()
with setting_tab:
    setting.setting()
with statistics_tab:
    statistics.statistics()

