def default_keyboard():
    '''
    Returns a dictionary that can be directly used to create a Keyboard object.
    '''
    return {
                                            "全消し" : 'All Clear',
                                            'BS' : 'Back Space'
                                            "log" : _input(r'\log_', target),
                                            '7' : _input(7, target),
                                            '8' : _input(8, target),
                                            '9' : _input(9, target),
                                            '÷' : _input(r"\div", target),
                                            'sin' : _input(r"\sin", target),
                                            'cos' : _input(r"\cos", target),
                                            'tan' : _input(r"\tan", target),
                                            '4' : _input(4, target),
                                            '5' : _input(5, target),
                                            '6' : _input(6, target),
                                            '×' : _input(r"\times", target),
                                            'π' : _input(r"\pi", target),
                                            'i' : _input("I", target),
                                            '√' : _input(r"\sqrt[2]", target),
                                            '1' : _input(1, target),
                                            '2' : _input(2, target),
                                            '3' : _input(3, target),
                                            'ー' : _input("-", target), # ASCII '-' doesn't get displayed??
                                            '(' : _input("{", target),
                                            ')' : _input("}", target),
                                            '累乗' : _input("^", target),
                                            '0' : _input(0, target),
                                            '.' : _input(".", target),
                                            '=' : _input("=", target),
                                            '＋' : _input("+", target), # Same as '-'
                                            ',' : _input(',', target)
                                           }
