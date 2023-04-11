import param
from enum import Enum

class Move(Enum):
    EMPTY = ' '
    X = 'X'
    O = 'O'

class Difficulty(Enum):
    EASY = 'Easy'
    INTERMEDIATE = 'Intermediate'
    PRO = 'Pro'

class GameStatus(Enum):
    DRAW = 'Draw'
    WIN = 'Win'
    IN_PROGRESS = 'In Progress'    

class Cell(param.Parameterized):
    winning_cell = param.Boolean(default=False)
    move = param.ObjectSelector(default=Move.EMPTY, objects=[Move.EMPTY, Move.X, Move.O])