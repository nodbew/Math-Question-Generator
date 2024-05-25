import numpy as np
import sympy as sy

class QuestionFormat:
    def __init__(self, fmt:list) -> None:
        """
        Converts a list into question format.
        fmt should be a list of CharacterGenerator, 
                                OperandGenerator, 
                                Operands(str),
                                NumberGeberator,
                                and numbers.
        """
        assert type(fmt) == list
        
        self._characters = dict()
        
        for i, elem in enumerate(fmt):
            if isinstance(elem, generators.CharacterGenerator):
                fmt[i] = elem.__next__()
                self._characters[fmt[i]] = sy.Symbol(fmt[i])
        
        self._callables = [elem for elem in fmt if callable(elem)]
        self._format = "".join("{}" if callable(elem) else elem for elem in fmt)
        return
        
    def generate(self) -> str:
        # Create a question string
        question = self._format.format(*[callable.__call__() for callable in self._callables])
        
        # Check the question is valid as a formula
        try:
            q = eval(question, {"__builtins__":None}, self._characters)
        except SyntaxError:
            raise SyntaxError("有効な問題形式ではありません")
        
        # Hold the answer for the question
        self._answer = sy.solve(a)
        
        return question