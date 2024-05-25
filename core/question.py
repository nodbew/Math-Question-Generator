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
        
        self._callables = [elem for elem in fmt if callable(elem)]
        self._format = "".join("{}" if callable(elem) else elem for elem in fmt)
        return
        
    def generate(self):
        question = self._format.format(*[callable.__call__() for callable in self._callables])
        try: