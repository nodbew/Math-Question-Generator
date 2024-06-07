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
        
    

def format_evaluate(input:str = None) -> str:
    if input is None:
        input = st.session_state.input
    else:
        input = st.session_state[input]

    if input == []:
        return []

    value_str = ''.join(str(elem) for elem in input).replace('{', '(').replace('}', ')')

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

    # Split with operands
    i = 0
    char_gen = generators.CharacterGenerator()
    fmt = re.split('([-+*/])', value_str)

    raise Exception(fmt)
    
    while i < len(fmt):
        print(i)
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

        if '^' in fmt[i]:
            fmt[i] = fmt[i].replace('^', '**')

        fmt[i] = fmt[i].replace('<', '＜').replace('>', '＞')
        
        match fmt[i].strip():
            case '＜乱数＞':
                fmt[i] = generators.NumberGenerator(low = -25, high = 25)
            case '＜計算記号＞':
                fmt[i] = st.session_state.OperandGenerator
            case '＜文字＞':
                fmt[i] = char_gen.__next__()
            case capture:
                pass

        i += 1

    return fmt
