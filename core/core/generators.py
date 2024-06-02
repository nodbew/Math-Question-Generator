import random
import numpy as np

class _BaseGenerator:
    '''
    A base class for all generators.
    Choses one element from the given choices list randomly, and returns it when called.
    '''
    def __init__(self, choices = []):
        self._choices = choices
        return

    def __call__(self):
        return random.choice(self._choices)

    def __next__(self):
        return self.__call__()
        
class OperandGenerator(_BaseGenerator):
    '''
    Generator object that returns a random operand from the given operands list.
    '''
    def __init__(self, operands = ['+', '-']):
        super().__init__(operands)
        return

class NumberGenerator(_BaseGenerator):
    '''
    Generator object that returns a random integer within the given range.
    '''
    def __init__(self, low:int = -25, high:int = 25):
        self._low = low
        self._high = high + 1 # np.random.Generator.integers doesn't return high
        self._generator = np.random.default_rng().integers
        return

    def __call__(self):
        return self._generator(low = self._low, high = self._high)

class CharacterGenerator(_BaseGenerator):
    '''
    Generator object that returns an unused alphabet. 
    It all alphabets are used, returns subscripted alphabets with latex-styled string.
    '''
    def __init__(self):
        self._current_ord = 97
        self._subscript = 0
        return

    def __call__(self):
        if self._subscript == 0:
            response = chr(self._current_ord)
        else:
            response = chr(self._current_ord) + '_' + str(self._subscript)
            
        self._current_ord += 1
        if self._current_ord == 123: # ord('z') == 122
            self._current_ord = 97
            self._subscript += 1

        return response

class SympyFunction:
    '''
    A class that holds a sympy function and its arguments.
    If an argument is callable, it will be replaced with the result of calling it.
    '''
    def __init__(self, sympy_func, *args, **kwargs):
        self._func = sympy_func
        self._args = args
        self._kwargs = kwargs 
        return

    def __call__(self):
        return self._func(
            *[arg.__call__() if callable(arg) else arg for arg in self._args],
            **{key:(value.__call__() if callable(value) else value) for key, value in self._kwargs.items()}
        )
