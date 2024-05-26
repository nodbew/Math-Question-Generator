import numpy as np
import sympy as sy

class QuestionFormat:
    def __init__(self, fmt:list) -> None:
        """
        Converts a list into question format.
        fmt should be a list of OperandGenerator, 
                                Operands(str),
                                NumberGeberator,
                                and numbers.
        """
        assert type(fmt) == list
        
        self._characters = {elem:sy.Symbol(elem) for elem in fmt if 97 <= ord(elem[0]) <= 122} # Extract alphabets from the list
        self._callables = [elem for elem in fmt if callable(elem)] # Split callables from others
        self._format = "".join("{}" if callable(elem) else elem for elem in fmt) # Use str.format afterward
        return
        
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
                q = eval(question, {"__builtins__":None}, characters)
            except SyntaxError:
                raise SyntaxError("有効な問題形式ではありません")
        
            # Hold the answer for the question
            try:
                self._answer = answer.calculate_answer(q)
            except answer.RegulationError:
                continue
            else:
                return question

        raise answer.RegulationError('条件に合う問題が見つかりませんでした  \n設定を変更するか、問題形式を変更してください')
