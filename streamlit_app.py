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
    # user settings
    st.session_state.settings = init.settings()
if 'OperandGenerator' not in st.session_state:
    # rng-like commonized random operator gen
    st.session_state.OperatorGenerator = init.operator_generator()
if 'input' not in st.session_state:
    # inputs from keyboard
    st.session_state.input = []
if 'input_keyboard' not in st.session_state:
    # commonized keyboard object
    st.session_state.input_keyboard = Keyboard(comp_init.default_keyboard(), target = 'input')
if 'format_input' not in st.session_state:
    # inputs for format, from another keyboard
    st.session_state.format_input = []
if 'format_keyboard' not in st.session_state:
    # a keyboard for inputting question format
    st.session_state.format_keyboard = Keyboard(comp_init.default_format_keyboard(), target = 'format_input')
if 'format_input_CharacterGenerator' not in st.session_state:
    # character gen for format input
    st.session_state.format_input_CharacterGenerator = init.character_generator()

# templates in a dict
if 'templates' not in st.session_state:
    st.session_state.templates = {
        '二次方程式の求解' : init.polynomial_problem(),
        '二次方程式の展開' : question.ExpansionQuestionFormat(init.polynomial_problem(raw_format = True)),
        '二次方程式の因数分解' : question.FactorizationQuestionFormat(init.polynomial_problem(raw_format = True)),
        '整数問題' : question.NumberQuestionFormat([generators.NumberGenerator(), st.session_state.OperatorGenerator, generators.NumberGenerator()])
    }
    
if 'current_template' not in st.session_state:
    # currently used templates
    st.session_state.current_template = st.session_state.templates['二次方程式の求解']
if 'current_question' not in st.session_state:
    # generate the first question
    st.session_state.current_question = st.session_state.current_template.generate()
if 'checked' not in st.session_state:
    # to respond to the "answer" button
    st.session_state.checked = False
if 'count' not in st.session_state:
    # global count of questions answered
    st.session_state.count = 0
if 'correct_count' not in st.session_state:
    # global count of questions correctly answered
    st.session_state.correct_count = 0
if 'start_time' not in st.session_state:
    # record of the init time
    st.session_state.start_time = datetime.datetime.now()

# Layouts of each tab are written in each file
import core.components.main_tab as main
import core.components.setting_tab as setting
import core.components.template_tab as template
import core.components.statistics_tab as statistics

# Create tab objects with names
main_tab, template_tab, setting_tab, statistics_tab = st.tabs(['出題', '問題形式', '設定', '統計'])

# See each file for detail
with main_tab:
    main.main()
with template_tab:
    template.template()
with setting_tab:
    setting.setting()
with statistics_tab:
    statistics.statistics()