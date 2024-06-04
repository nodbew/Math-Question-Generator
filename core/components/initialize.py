import streamlit as st

from ..core import generators

def default_keyboard():
    '''
    Returns a dictionary that can be directly used to create a Keyboard object.
    '''
    return {
        "全消し" : 'All Clear',
        'BS' : 'Back Space',
        "log" : (r'\log_'),
        '7' : (7),
        '8' : (8),
        '9' : (9),
        '÷' : (r"\div"),
        'sin' : (r"\sin"),
        'cos' : (r"\cos"),
        'tan' : (r"\tan"),
        '4' : (4),
        '5' : (5),
        '6' : (6),
        '×' : (r"\times"),
        'π' : (r"\pi"),
        'i' : ("I"),
        '√' : (r"\sqrt[2]"),
        '1' : 1,
        '2' : (2),
        '3' : (3),
        'ー' : ("-"), # ASCII '-' not displayed properly??
        '(' : ("{"),
        ')' : ("}"),
        '累乗' : ("^"),
        '0' : (0),
        '.' : ("."),
        '=' : ("="),
        '＋' : ("+"), # Same as '-'
        ',' : ',',
        '°' : r'^{\circ}'
    }

def default_format_keyboard():
    '''
    Based on default_keyboard, adds some additional keys for creating QuestionFormat object.
    '''
    default = default_keyboard()
    character_generator = generators.CharacterGenerator()
    additional = {
        '乱数' : generators.NumberGenerator(),
        '文字' : character_generator,
        '記号' : st.session_state.OperandGenerator,
    }
    return default | additional
