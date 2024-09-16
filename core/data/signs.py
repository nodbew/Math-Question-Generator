"""
Constant values used in the code
"""

CALCULATION_SIGNS = ('+', '-', '*', '/', '^', r'^{\circ}', r'\times', r'\div')
BRACKETS = ('{', '}', ',')
FUNCTIONS = (r'\log_', r'\sin', r'\cos', r'\tan', r'\sqrt[2]')
CONSTANTS = (r'\pi', 'I')

CALCULATIONS = CALCULATION_SIGNS + BRACKETS
OPERATORS_AND_FUNCTIONS = CALCULATION_SIGNS + ('{',) + FUNCTIONS
MATH_SYMBOLS = FUNCTIONS + CONSTANTS

SPECIALS = CALCULATION_SIGNS + BRACKETS + FUNCTIONS + CONSTANTS
