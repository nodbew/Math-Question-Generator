import re

import sympy as sy
import streamlit as st

from . import generators
from ..data import signs
from .error_handler import error_handler

class SettingViolation(Exception):pass
class RegulationError(Exception):pass

def calculate_answer(evaluated_question, solve_char):
    '''
    Takes number, sy.Expr or other valid question. The question should be evaluated, and should not be a str.
    Returns the answer for it.

    The answer will be checked based on the settings, and if there is a fault, RegulationError will be raised.
    '''
    if not isinstance(evaluated_question, sy.Expr):
        # Number problem is already calculated when evaluating
        return evaluated_question

    else:
        # Sympy Expr
        # Answer and settings
        answers = sy.solve(evaluated_question, sy.Symbol(solve_char))

        # Complex answers
        if not st.session_state.settings['複素数解を許容する']:
            answers = [ans for ans in answers if not ans.has(sy.I)]
            if len(answers) == 0:
                raise SettingViolation('設定違反：虚数解')

        return answers
        
def parse(input:str = None):
    '''
    Parse the recorded user input and returns a latex string.
    return ''.join(st.session_state._input)
    '''
    
    if input is None:
        input = st.session_state.input
    else:
        input = st.session_state[input]
    
    result = " ".join(str(elem) for elem in input)
    result = result.replace("**", "^").replace('*', '').replace('I', 'i')

    return result

def _change_to_str(input) -> str:
    if input is None:
        input = st.session_state.input
    else:
        input = st.session_state[input]

    if input == []:
        return ''

    st.write(input)

    value_str = ''.join(elem if isinstance(elem, str) else repr(elem) for elem in input).replace('{', '(').replace('}', ')')

    # Check unterminated parenthesis
    if input[-1] != '}':
        value_str += ')'

    # Replace degree with radian
    value_str = re.sub(r'(\d+)^{[\\]circ}', 'sy.rad<\1>', value_str)

    # Replace the latex log function with a pythonic function styled str
    value_str = re.sub(r'[\\]log_\((\d+?)\)*\((\d+?)\)', r'sy.log<\2, \1>', value_str)
        
    # Replace latex sqrt with math.sqrt function
    value_str = re.sub(r'[\\]sqrt\[2\]\((\d+?)\)', r'sy.sqrt<\1>', value_str)

    # Replace constants
    value_str = value_str.replace(r'\pi', 'sy.pi').replace('I', 'sy.I')

    # Replace calculation signs
    value_str = value_str.replace(r'\times', '*').replace(r'\div', '/')

    # Replace sympy functions with generator.SympyFunction object
    value_str = re.sub(r'sy\.(.+?)<(.+?)>', r'SympyFunction(sy.(\1), (\2))', value_str)

    return value_str

@error_handler
def format_evaluate(input:str = None) -> list:
    value_str = _change_to_str(input)
    
    # Split with operands
    i = 0
    fmt = re.split('([-+*/()])', value_str)
    # For evaluating
    gl0bals = {
        'OperatorGenerator' : generators.OperatorGenerator,
        'NumberGenerator' : generators.NumberGenerator,
        'CharacterGenerator' : generators.CharacterGenerator,
        'SympyFunction' : generators.SympyFunction,
    }

    while i < len(fmt):
        # Organize
        fmt[i] = fmt[i].strip()
        fmt[i] = fmt[i].replace('ー', '-').replace('＋', '+').replace('＊', '*').replace('・', '/')
        if '^' in fmt[i]:
            fmt[i] = fmt[i].replace('^', '**')

        # Evaluate objects
        if fmt[i] in (signs.FUNCTIONS + ('OperatorGenerator', 'NumberGenerator', 'CharacterGenerator', 'SympyFunction')):

            if fmt[i + 1].strip() != '(':
                raise SyntaxError('関数の直後にはカッコが必要です')

            if ')' not in fmt[i + 2:]:
                raise SyntaxError('カッコが閉じられていません')
                
            else:
                closing_parenthesis = fmt[i + 2:].index(')')
                fmt[i] = ''.join(fmt[i : i + closing_parenthesis + 3]).replace('ー', '-').replace('＋', '+').replace('＊', '*').replace('・', '/')
                fmt = fmt[:i + 1] + fmt[i + closing_parenthesis + 3:]

            st.write(fmt[i])
            fmt[i] = eval(fmt[i], gl0bals, {}) # generators.Generator object

        i += 1
        continue

    return fmt

@error_handler
def evaluate(input:str = None) -> list:
    value_str = _change_to_str(input)
    
    # Split with operands
    i = 0
    fmt = re.split('([-+*/()])', value_str)

    while i < len(fmt):
        # Organize
        fmt[i] = fmt[i].strip()
        fmt[i] = fmt[i].replace('ー', '-').replace('＋', '+').replace('＊', '*').replace('・', '/')
        if '^' in fmt[i]:
            fmt[i] = fmt[i].replace('^', '**')

        # Evaluate objects
        if fmt[i] in signs.FUNCTIONS:

            if fmt[i + 1].strip() != '(':
                raise SyntaxError('関数の直後にはカッコが必要です')

            if ')' not in fmt[i + 2:]:
                raise SyntaxError('カッコが閉じられていません')
                
            else:
                closing_parenthesis = fmt[i + 2:].index(')')
                fmt[i] = ''.join(fmt[i : i + closing_parenthesis + 3]).replace('ー', '-').replace('＋', '+').replace('＊', '*').replace('・', '/')
                fmt = fmt[:i + 1] + fmt[i + closing_parenthesis + 3:]

            fmt[i] = eval(fmt[i], {__builtins__:None, "sy":sy}, {}) # generators.Generator object

        i += 1
        continue

    return fmt