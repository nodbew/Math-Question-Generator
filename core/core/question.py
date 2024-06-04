import numpy as np
import sympy as sy

from . import answer
from . import error_handler

class QuestionFormat:
    def __init__(self, fmt:list) -> None:
        """
        Converts a list into question format.
        fmt should be a list of OperandGenerator, 
                                Operands(str),
                                NumberGeberator,
                                numbers(int),
                                and generators.SympyFunction object.
        """
        assert type(fmt) == list
        
        self._characters = {elem:sy.Symbol(elem) for elem in fmt if (type(elem) == str and 97 <= ord(elem[0]) <= 122)} # Extract alphabets from the list
        self._callables = [elem for elem in fmt if callable(elem)] # Split callables from others
        self._format = "".join("{}" if callable(elem) else str(elem) for elem in fmt) # Use str.format afterward

        if len(self._characters) == 0:
            self._solve_char = None
            self.QUESTION = 'この問題を解きなさい'
        else:
            self._solve_char = min(self._characters.keys(), key = ord)
            self.QUESTION = f'この問題を{self._solve_char}について解きなさい'
        return

    @error_handler.error_handler
    def generate(self) -> str:
        '''
        Try to generate a question that fits the settings until it reaches the recursion limit.
        Recursion limit is set because it is hard to detect "ungenerateable" problems, and it is 50.
        
        This method basically substitutes actual values(e.g. numbers, operands) into the format string.
        Then, evaluates it and calculates the answer.
        '''
        callables = self._callables
        characters = self._characters
        
        for _ in range(50): # Recursion limit
            # Create a question string
            question = self._format.format(*[callable.__call__() for callable in callables])
        
            # Check the question is valid as a formula
            try:
                q = eval(question, {"__builtins__":None, 'sy':sy}, characters)
            except SyntaxError:
                raise SyntaxError("有効な問題形式ではありません")
        
            # Hold the answer for the question
            try:
                self._answer = answer.calculate_answer(q, self._solve_char)
            except answer.SettingViolation:
                continue
            else:
                return q

        raise answer.RegulationError('条件に合う問題が見つかりませんでした  \n設定を変更するか、問題形式を変更してください')

    def check(self, ans) -> bool:
        '''
        Parses the answer in an appropriate way and checks the answer.
        '''
        if answer.parse(answer) == self._answer:
            return True
        else:
            return False

class ExpansionQuestionFormat(QuestionFormat):
    '''
    Answer calculation has one more step in this class, that is, expanding a polynomial formula.
    '''
    def generate(self):
        question = super().generate()
        self._answer = [sy.expand(question)]
        return question

class FactorizationQuestionFormat(QuestionFormat):
    '''
    Factorized formula will be the answer.
    '''
    def generate(self):
        question = super().generate()
        self._answer = [sy.factor(question)]
        return question
