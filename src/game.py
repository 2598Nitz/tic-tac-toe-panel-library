import random
import param
import time
from model import Cell,Move
from consts import BOARD_DIMENSION,COMPUTER_DELAY_SEC

class TicTacToe(param.Parameterized):
    """Represents a Tic Tac Toe game board.

    This class provides methods to make moves on the board, check if the game has ended and determine the winner.
    The board is represented as a 2D list of Cell objects, where each cell can either be empty, have a move from player X or a move from player O.

    Attributes:
        board (list[list[Cell]]): The board state represented as a 2D list of Cell objects.
        current_move (Move): The move of the current player (either Move.X or Move.O).
        game_ended (bool): A flag indicating if the game has ended.
        winner (Move): The move of the winning player (either Move.X or Move.O), or Move.EMPTY if there is no winner yet.

    Methods:
        reset_game_state(): Resets the board and game state to their initial values.
        make_move(row, col): Makes a move on the board at the specified row and column if it's a valid move.
        __switch_player(): Switches the current player to the other player Eg. X to O. 
        __make_computer_move(): Makes a move for the computer player (Move.O).
        __check_game_ended(): Checks if the game has ended and updates the winner and game_ended attributes accordingly.
        __get_available_moves(): Returns a list of available moves on the board.
        __check_end_condition_by_moves(move1, move2, move3): Checks if the three given moves are equal and not empty.
    """    
    board = param.List([[Cell() for i in range(BOARD_DIMENSION)] for j in range(BOARD_DIMENSION)])
    current_move = param.Selector(objects=[Move.X, Move.O], default=Move.X)
    game_ended = param.Boolean(default=False)
    winner = param.ClassSelector(class_=Move, default=Move.EMPTY)
    
    def reset_game_state(self):
        self.board = [[Cell() for i in range(BOARD_DIMENSION)] for j in range(BOARD_DIMENSION)]
        self.current_move = Move.X
        self.game_ended = False
        self.winner = Move.EMPTY

    def make_move(self, row, col):
        if self.board[row][col].move is not Move.EMPTY or self.game_ended:
            return
        self.board[row][col] = Cell(move=self.current_move)
        self.__check_game_ended()
        self.__switch_player()
        if self.current_move == Move.O and not self.game_ended:
            self.__make_computer_move()
    
    def __switch_player(self):
        self.current_move = Move.O if self.current_move == Move.X else Move.X
    
    def __make_computer_move(self):
        time.sleep(COMPUTER_DELAY_SEC)
        available_moves = self.__get_available_moves()
        if not available_moves:
            return
        row, col = random.choice(available_moves)
        self.make_move(row, col)
    
    def __check_game_ended(self):
        # Check rows
        for row in range(BOARD_DIMENSION):
            if self.__check_end_condition_by_moves(self.board[row][0].move, self.board[row][1].move, self.board[row][2].move):
                self.game_ended = True
                self.winner = self.board[row][0].move
                self.board[row][0].winning_cell = self.board[row][1].winning_cell = self.board[row][2].winning_cell = True
                return
        # Check columns
        for col in range(BOARD_DIMENSION):
            if self.__check_end_condition_by_moves(self.board[0][col].move, self.board[1][col].move, self.board[2][col].move):
                self.game_ended = True
                self.winner = self.board[0][col].move
                self.board[0][col].winning_cell = self.board[1][col].winning_cell = self.board[2][col].winning_cell = True
                return
        # Check diagonals
        if self.__check_end_condition_by_moves(self.board[0][0].move, self.board[1][1].move, self.board[2][2].move):
            self.game_ended = True
            self.winner = self.board[0][0].move
            self.board[0][0].winning_cell = self.board[1][1].winning_cell = self.board[2][2].winning_cell = True
            return
        if self.__check_end_condition_by_moves(self.board[0][2].move, self.board[1][1].move, self.board[2][0].move):
            self.game_ended = True
            self.winner = self.board[0][2].move
            self.board[0][2].winning_cell = self.board[1][1].winning_cell = self.board[2][0].winning_cell = True
            return
        # Game Draw
        if not self.__get_available_moves():
            self.game_ended = True
            return

    def __get_available_moves(self):
        available_moves = []
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                if self.board[row][col].move is Move.EMPTY:
                    available_moves.append((row, col))
        return available_moves

    def __check_end_condition_by_moves(self, move1: Move, move2: Move, move3: Move):
        return move1 == move2 and move2 == move3 and move1 is not Move.EMPTY