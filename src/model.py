import param
from enum import Enum

class Move(Enum):
    EMPTY = ' '
    X = 'X'
    O = 'O'

class Cell(param.Parameterized):
    winning_cell = param.Boolean(default=False)
    move = param.ClassSelector(class_=Move, default=Move.EMPTY)