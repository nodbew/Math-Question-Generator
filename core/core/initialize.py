from collections.abc import Iterable

import streamlit as st

from . import generators
from . import question as question

def settings():
    return {
        '複素数解を許容する' : False
    }

def operand_generator():
    return generators.OperandGenerator()

def _flatten(iterable):
    raise Exception(repr(iterable))
    for elem in iterable:
        if type(iterable) == list or type(iterable) == tuple:
            yield from _flatten(elem)
        else:
            yield elem

def polynomial_problem(element : int = 1, dimension : int = 2, raw_format = False):
    '''
    A convenience function to create questions of polynomial formula.
    This is a convenience class to create a polynomial problem. Thus, it doesn't offer any new features.
    '''
    # Generate characters
    character_generator = generators.CharacterGenerator()
    characters = [character_generator.__next__() for _ in range(element)]

    # Format
    dimension += 1 # dimension will be used in range(), therfore it has to be added by one
    random_symbol = st.session_state.OperandGenerator
    format = [[generators.NumberGenerator(), '*', character, '**', dim, random_symbol.__next__]
                for dim in range(dimension)
                for character in characters] 
    
    if raw_format:
        return list(_flatten(format))[:-1]# Remove calculation symbol at the end of the list
    else:
        return question.QuestionFormat(list(_flatten(format))[:-1])
