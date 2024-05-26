import sympy as sy
import streamlit as st

class RegulationError(Exception):pass

def calculate_answer(evaluated_question):
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
        answers = sy.solve(evaluated_question, sy.Symbol('a'))
        settings = st.session_state.settings

        # Complex answers
        if not settings['虚数解を許容する']:
            answers = [ans for ans in answers if ans.has(sy.I)]
            if len(answers) == 0:
                raise RegulationError('設定違反：虚数解')

        return answers
