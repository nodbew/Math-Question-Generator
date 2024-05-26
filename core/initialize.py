from .generators import OperandGenerator

def settings():
    return {
        '複素数解を許容する' : False
    }

def operand_generator():
    return OperandGenerator()
