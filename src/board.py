from model import Cell, Move, GameStatus
from consts import BOARD_DIMENSION

class Board:
    """
    The Board class represents the game board of TicTacToe.

    Attributes:
        __board_grid (list[list[Cell]]): A 2D list of Cell representing the current state of the board.
    
    Methods:
        __init__(board_grid=None): Initializes a new Board object with a given board grid.
        get_available_moves(): Returns a list of available moves, represented as tuples of row and column indices.
        get_game_state(): Returns the current state of the game, represented as a tuple of GameStatus and additional information if GameStatus is WIN.
        __check_end_condition_by_moves(move1: Move, move2: Move, move3: Move): Returns True if three given moves are same and not empty.
        get_board_grid(): Returns the 2D game board.
        get_cell(row, col): Returns the Cell object at a given row and column for game board.
        set_cell(row, col, move, winning_cell=False): Sets the move for a given cell and sets it as a winning cell if specified.
    """

    def __init__(self, board_grid=None):
        if board_grid:
            self.__board_grid = [[Cell(move=board_grid[row][col].move) for col in range(BOARD_DIMENSION)] for row in range(BOARD_DIMENSION)]
        else:  
            self.__board_grid = [[Cell() for col in range(BOARD_DIMENSION)] for row in range(BOARD_DIMENSION)]

    def reset_board(self):
        self.__board_grid = [[Cell() for col in range(BOARD_DIMENSION)] for row in range(BOARD_DIMENSION)]

    def get_available_moves(self):
        available_moves = []
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                if self.__board_grid[row][col].move is Move.EMPTY:
                    available_moves.append((row, col))
        return available_moves
    
    def get_game_state(self):
        '''
        Returns the current state of the game, represented as a tuple of GameStatus and additional information if GameStatus is WIN.
        Additional information includes winning move marker and 3 cell indexes which are part of the win represented as tuple of row,col.
        '''

        # Check rows
        for row in range(BOARD_DIMENSION):
            if self.__check_end_condition_by_moves(self.__board_grid[row][0].move, self.__board_grid[row][1].move, self.__board_grid[row][2].move):
                return (GameStatus.WIN, self.__board_grid[row][0].move, ((row,0), (row,1), (row,2),))
        # Check columns
        for col in range(BOARD_DIMENSION):
            if self.__check_end_condition_by_moves(self.__board_grid[0][col].move, self.__board_grid[1][col].move, self.__board_grid[2][col].move):
                return (GameStatus.WIN, self.__board_grid[0][col].move, ((0,col), (1,col), (2,col),))
        # Check diagonals
        if self.__check_end_condition_by_moves(self.__board_grid[0][0].move, self.__board_grid[1][1].move, self.__board_grid[2][2].move):
            return (GameStatus.WIN, self.__board_grid[0][0].move, ((0,0), (1,1), (2,2),))
        if self.__check_end_condition_by_moves(self.__board_grid[0][2].move, self.__board_grid[1][1].move, self.__board_grid[2][0].move):
            return (GameStatus.WIN, self.__board_grid[0][2].move, ((0,2), (1,1), (2,0),))
        # Game Draw
        if not self.get_available_moves():
            return (GameStatus.DRAW,)
        return (GameStatus.IN_PROGRESS,)
        
    def __check_end_condition_by_moves(self, move1: Move, move2: Move, move3: Move):
        return move1 == move2 and move2 == move3 and move1 is not Move.EMPTY
    
    def get_board_grid(self):
        return self.__board_grid
    
    def get_cell(self, row, col):
        return self.__board_grid[row][col]
    
    def set_cell(self, row, col, move, winning_cell = False):
        self.__board_grid[row][col].move = move
        self.__board_grid[row][col].winning_cell = winning_cell
