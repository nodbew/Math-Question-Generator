import re

import sympy as sy
import streamlit as st

from . import generators

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
        return []

    value_str = ''.join(repr(elem) for elem in input).replace('{', '(').replace('}', ')')

    # Check unterminated parenthesis
    if type(input[-1]) == int:
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
    value_str = re.sub(r'sy\.(.+?)<(.+?)>', r'generators.SympyFunction(sy.(\1), (\2))', value_str)

    return value_str

def format_eval(input:str = None) -> list:
    value_str = _change_to_str(input)
    
    # Split with operands
    i = 0
    fmt = re.split('([-+*/])', value_str)
    
    while i < len(fmt):
        # Organize
        fmt[i] = fmt[i].strip()
        if '^' in fmt[i]:
            fmt[i] = fmt[i].replace('^', '**')

        # Evaluate objects
        if fmt[i].strip().startswith('generators.SympyFunction('):
            fmt[i] = fmt[i].strip()
            
            # generators.SympyFunction(sy.sin, (27) * (3)) -> ['generators.SympyFunction(sy.sin, (27)', '*', '(3))']
            parenthesis = len(fmt[i]) - len(fmt[i].lstrip('(')) # Number of parenthesis
            if not fmt[i].endswith(')'*parenthesis):
                j = i
                while not fmt[j].endswith(')'*parenthesis):
                    j += 1
                for _ in range(j):
                    fmt[i] += fmt.pop(i + 1)

                fmt[i] = eval(fmt[i]) # generators.SympyFunciton object

            i += 1
            continue

        try:
            fmt[i] = eval(fmt[i])
            i += 1
            continue
        except SyntaxError:
            i += 1
            continue

    raise Exception(fmt)

    return fmt
