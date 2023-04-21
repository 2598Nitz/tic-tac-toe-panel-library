import random
import math 

from board import Board
from model import Move,GameStatus
from consts import BOARD_DIMENSION

######## ALGORITHMS FOR COMPUTER'S NEXT MOVE ############

def get_random_next_move(available_moves):
    return random.choice(available_moves)

def get_non_best_move(available_moves, best_move):
    if len(available_moves) == 1:
        return best_move
    non_best_moves = list(filter(lambda move: move != best_move, available_moves))
    return random.choice(non_best_moves)

def get_best_move(available_moves, board: Board, computerMarker: Move):
    best_score = -math.inf
    best_move = None
    if len(available_moves) == BOARD_DIMENSION*BOARD_DIMENSION:
        best_move = (0,0) #Optimization for empty grid
    else:
        for (row,col) in available_moves:
            board.set_cell(row,col,computerMarker)
            score = minimax(False, board, computerMarker)
            board.set_cell(row,col,Move.EMPTY)
            if (score > best_score):
                best_score = score
                best_move = (row,col) 

    return best_move

def minimax(is_max_turn, board: Board, maximizeMarker: Move):
    state = board.get_game_state()
    if state[0] == GameStatus.DRAW:
        return 0
    elif state[0] == GameStatus.WIN:
        return 1 if state[1] == maximizeMarker else -1

    scores = []
    for (row,col) in board.get_available_moves():
        minimize_marker = Move.X if maximizeMarker == Move.O else Move.O
        if is_max_turn:
            board.set_cell(row,col,maximizeMarker)
        else:
            board.set_cell(row,col,minimize_marker)
        scores.append(minimax(not is_max_turn, board, maximizeMarker))
        board.set_cell(row,col,Move.EMPTY)
        if (is_max_turn and max(scores) == 1) or (not is_max_turn and min(scores) == -1):
            break

    return max(scores) if is_max_turn else min(scores)