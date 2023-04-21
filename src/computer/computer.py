import random
import time
from abc import ABC, abstractmethod

from model import Difficulty,Move
from board import Board
from consts import COMPUTER_DELAY_SEC
from .utils import *

class ComputerInterface(ABC):
    '''
    All implementations of ComputerInterface will provide get_move method to make next computer move.
    '''

    @abstractmethod
    def get_move(self, board: Board, computerMarker: Move):
        pass


class BeginnerComputer(ComputerInterface):
    '''
    Beginner Computer which randomly selects next move from available moves.
    '''

    def get_move(self, board: Board, computerMarker: Move):
        time.sleep(COMPUTER_DELAY_SEC)
        return get_random_next_move(board.get_available_moves())
    

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
        self.__mistake_probability = 0.5

    def get_move(self, board: Board, computerMarker: Move):
        time.sleep(COMPUTER_DELAY_SEC)
        available_moves = board.get_available_moves()
        make_mistake = random.random() < self.__mistake_probability
        best_move = get_best_move(available_moves, board, computerMarker)
        if make_mistake:
            self.__mistake_probability = 0
            return get_non_best_move(available_moves, best_move)
        else:
            if self.__mistake_probability != 0:
                self.__mistake_probability = min(1, self.__mistake_probability+0.15)
            return best_move
        

class ExpertComputer(ComputerInterface):
    '''
    Expert Computer which always makes optimal move. Not possible to defeat this computer.
    For making optimal move, minimax algorithm is used.
    '''

    def get_move(self, board: Board, computerMarker: Move):
        time.sleep(COMPUTER_DELAY_SEC)
        return get_best_move(board.get_available_moves(), board, computerMarker)
    

class ComputerFactory:
    '''
    Factory class to get computer implementation by game difficulty.
    '''
    @staticmethod
    def get_computer_by_difficulty(difficulty: Difficulty):
        if difficulty == Difficulty.EASY:
            return BeginnerComputer()
        elif difficulty == Difficulty.INTERMEDIATE:
            return IntermediateComputer()
        else:
            return ExpertComputer()        
        