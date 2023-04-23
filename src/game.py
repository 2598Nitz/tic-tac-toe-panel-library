import param
from model import Move,Difficulty,GameStatus
from computer.computer import ComputerInterface, BeginnerComputer, ComputerFactory
from board import Board

class TicTacToe(param.Parameterized):
    """
    Represents Tic Tac Toe game controller.
    This class provides methods to make moves on the board, reset game state. 

    Methods:
        reset_game_state(): Resets the board and game state to their initial values.
        make_move(row, col): Makes a move on the board at the specified row and column if it's a valid move.
        __update_game_state_on_move(gameState): Update game state like game_ended based on current board state. 
        __make_computer_move(): Makes a move for the computer player.
        __switch_player(): Switches the current player to the other player Eg. X to O.
        __switch_first_mover(): On every game reset, first mover is switched to add fairness to the game.
        __get_computer_move_marker(): Gives current move marker assigned to computer.
    """
    first_mover = param.Selector(objects=[Move.X, Move.O], default=Move.X, doc='Player who will make first move', precedence=-1)    
    current_move = param.Selector(objects=[Move.X, Move.O], default=Move.X, doc='The move of the current player', precedence=-1)
    user_move_marker = param.Selector(objects=[Move.X, Move.O], default=Move.X, doc='Move Marker selected by user')
    game_ended = param.Boolean(default=False, doc='A flag indicating if the game has ended', precedence=-1)
    winner = param.Selector(objects=[Move.X, Move.O, Move.EMPTY], default=Move.EMPTY, doc='The move of the winning player \
                            (either Move.X or Move.O), or Move.EMPTY if there is no winner yet', precedence=-1)
    board = param.ClassSelector(class_=Board, default=Board(), instantiate=True, doc='Object having board 2D grid, provides \
                                 methods to update game board and also provides game status', precedence=-1)
    difficulty = param.Selector(default=Difficulty.EASY, objects=[Difficulty.EASY, Difficulty.INTERMEDIATE, Difficulty.PRO], \
                                doc='Difficulty level selected by user')
    computer = param.ClassSelector(class_=ComputerInterface, default=BeginnerComputer(), instantiate=True, \
                                   doc='ComputerInterface implementation object providing next move by computer', precedence=-1)

    def reset_game_state(self):
        self.board.reset_board()
        self.computer = ComputerFactory.get_computer_by_difficulty(self.difficulty)
        self.__switch_first_mover()
        self.current_move = self.first_mover
        self.game_ended = False
        self.winner = Move.EMPTY
        if self.current_move == self.__get_computer_move_marker():
            self.__make_computer_move()

    def make_move(self, row, col):
        if self.board.get_cell(row,col).move is not Move.EMPTY or self.game_ended:
            return
        
        self.board.set_cell(row,col,self.current_move)
        gameState = self.board.get_game_state()
        self.__update_game_state_on_move(gameState)

        if self.game_ended:
            return
        
        self.__switch_player()
        if self.current_move == self.__get_computer_move_marker():
            self.__make_computer_move()

    def __update_game_state_on_move(self, gameState):
        if gameState[0] == GameStatus.WIN:
            for (row,col) in gameState[2]:
                self.board.set_cell(row, col, gameState[1], True)
            self.winner = gameState[1]
            self.game_ended = True
        elif gameState[0] == GameStatus.DRAW:
            self.game_ended = True

    def __make_computer_move(self):
            (row,col) = self.computer.get_move(Board(self.board.get_board_grid()), self.__get_computer_move_marker())
            self.make_move(row, col)
    
    def __switch_player(self):
        self.current_move = Move.O if self.current_move == Move.X else Move.X
    
    def __switch_first_mover(self):
        self.first_mover = Move.O if self.first_mover == Move.X else Move.X

    def __get_computer_move_marker(self):
        return Move.X if self.user_move_marker == Move.O else Move.O
