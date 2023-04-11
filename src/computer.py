from model import Difficulty,GameStatus,Move
from board import Board
from consts import BOARD_DIMENSION,COMPUTER_DELAY_SEC
import random
import math
import time

class ComputerInterface:
    '''
    All implementations of ComputerInterface will provide get_move method to make next computer move.
    '''

    def get_move(self, board: Board, computerMarker: Move):
        pass


class BeginnerComputer(ComputerInterface):
    '''
    Beginner Computer which randomly selects next move from available moves.
    '''

    def get_move(self, board: Board, computerMarker: Move):
        time.sleep(COMPUTER_DELAY_SEC)
        available_moves = board.get_available_moves()
        return get_random_next_move(available_moves)
    

class IntermediateComputer(ComputerInterface):
    '''
    Intermediate Computer which for a game can return maximum one non-optimal (mistake) move.
    For making optimal move, minimax algorithm is used.
    For making non-optimal move, random available move excluding optimal move is selected.
    Whether next move will be optimal is decided by mistake_probability.
    If computer keeps making optimal move, mistake_probability is increased by 0.15 to ensure computer will make mistake soon.
    Once mistake is done, mistake_probability is reset to 0 to not allow further mistakes.
    '''

    def __init__(self):
        self.mistake_probability = 0.5

    def get_move(self, board: Board, computerMarker: Move):
        time.sleep(COMPUTER_DELAY_SEC)
        available_moves = board.get_available_moves()
        make_mistake = random.random() <= self.mistake_probability
        best_move = get_best_move(board.get_available_moves(), board, computerMarker)
        if make_mistake:
            self.mistake_probability = 0
            return get_non_best_move(available_moves, best_move)
        else:
            if self.mistake_probability != 0:
                self.mistake_probability = min(1, self.mistake_probability+0.15)
            return best_move
        

class ExpertComputer(ComputerInterface):
    '''
    Expert Computer which always makes optimal move. Not possible to defeat this computer.
    For making optimal move, minimax algorithm is used.
    '''

    def get_move(self, board: Board, computerMarker: Move):
        time.sleep(COMPUTER_DELAY_SEC)
        return get_best_move(board.get_available_moves(), board, computerMarker)


def get_computer_by_difficulty(difficulty: Difficulty):
    '''
    Factory method to get computer implementation by game difficulty.
    '''

    if difficulty == Difficulty.EASY:
        return BeginnerComputer()
    elif difficulty == Difficulty.INTERMEDIATE:
        return IntermediateComputer()
    else:
        return ExpertComputer()


######## ALGORITHMS FOR COMPUTER'S NEXT MOVE ############

def get_random_next_move(available_moves):
    return random.choice(available_moves)

def get_non_best_move(available_moves, best_move):
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
        