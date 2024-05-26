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
