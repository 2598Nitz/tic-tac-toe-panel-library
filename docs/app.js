importScripts("https://cdn.jsdelivr.net/pyodide/v0.22.1/full/pyodide.js");

function sendPatch(patch, buffers, msg_id) {
  self.postMessage({
    type: 'patch',
    patch: patch,
    buffers: buffers
  })
}

async function startApplication() {
  console.log("Loading pyodide!");
  self.postMessage({type: 'status', msg: 'Loading pyodide'})
  self.pyodide = await loadPyodide();
  self.pyodide.globals.set("sendPatch", sendPatch);
  console.log("Loaded!");
  await self.pyodide.loadPackage("micropip");
  const env_spec = ['https://cdn.holoviz.org/panel/0.14.3/dist/wheels/bokeh-2.4.3-py3-none-any.whl', 'https://cdn.holoviz.org/panel/0.14.3/dist/wheels/panel-0.14.3-py3-none-any.whl', 'pyodide-http==0.1.0', 'param']
  for (const pkg of env_spec) {
    let pkg_name;
    if (pkg.endsWith('.whl')) {
      pkg_name = pkg.split('/').slice(-1)[0].split('-')[0]
    } else {
      pkg_name = pkg
    }
    self.postMessage({type: 'status', msg: `Installing ${pkg_name}`})
    try {
      await self.pyodide.runPythonAsync(`
        import micropip
        await micropip.install('${pkg}');
      `);
    } catch(e) {
      console.log(e)
      self.postMessage({
	type: 'status',
	msg: `Error while installing ${pkg_name}`
      });
    }
  }
  console.log("Packages loaded!");
  self.postMessage({type: 'status', msg: 'Executing code'})
  const code = `
  
import asyncio

from panel.io.pyodide import init_doc, write_doc

init_doc()

import param
import panel as pn
from enum import Enum
import random
import math
import time

BOARD_DIMENSION = 3
GRID_SIZE = 300
GAME_MESSAGE_WIDTH = 400
GRID_BUTTON_SIZE = 100
COMPUTER_DELAY_SEC = 0.5

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

class Board:
    """
    The Board class represents the game board of TicTacToe.

    Attributes:
        board_grid (list[list[Cell]]): A 2D list of Cell representing the current state of the board.
    
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
            self.board_grid = [[Cell(move=board_grid[row][col].move) for col in range(BOARD_DIMENSION)] for row in range(BOARD_DIMENSION)]
        else:  
            self.board_grid = [[Cell() for col in range(BOARD_DIMENSION)] for row in range(BOARD_DIMENSION)]

    def reset_board(self):
        self.board_grid = [[Cell() for col in range(BOARD_DIMENSION)] for row in range(BOARD_DIMENSION)]

    def get_available_moves(self):
        available_moves = []
        for row in range(BOARD_DIMENSION):
            for col in range(BOARD_DIMENSION):
                if self.board_grid[row][col].move is Move.EMPTY:
                    available_moves.append((row, col))
        return available_moves
    
    def get_game_state(self):
        '''
        Returns the current state of the game, represented as a tuple of GameStatus and additional information if GameStatus is WIN.
        Additional information includes winning move marker and 3 cell indexes which are part of the win represented as tuple of row,col.
        '''

        # Check rows
        for row in range(BOARD_DIMENSION):
            if self.__check_end_condition_by_moves(self.board_grid[row][0].move, self.board_grid[row][1].move, self.board_grid[row][2].move):
                return (GameStatus.WIN, self.board_grid[row][0].move, ((row,0), (row,1), (row,2),))
        # Check columns
        for col in range(BOARD_DIMENSION):
            if self.__check_end_condition_by_moves(self.board_grid[0][col].move, self.board_grid[1][col].move, self.board_grid[2][col].move):
                return (GameStatus.WIN, self.board_grid[0][col].move, ((0,col), (1,col), (2,col),))
        # Check diagonals
        if self.__check_end_condition_by_moves(self.board_grid[0][0].move, self.board_grid[1][1].move, self.board_grid[2][2].move):
            return (GameStatus.WIN, self.board_grid[0][0].move, ((0,0), (1,1), (2,2),))
        if self.__check_end_condition_by_moves(self.board_grid[0][2].move, self.board_grid[1][1].move, self.board_grid[2][0].move):
            return (GameStatus.WIN, self.board_grid[0][2].move, ((0,2), (1,1), (2,0),))
        # Game Draw
        if not self.get_available_moves():
            return (GameStatus.DRAW,)
        return (GameStatus.IN_PROGRESS,)
        
    def __check_end_condition_by_moves(self, move1: Move, move2: Move, move3: Move):
        return move1 == move2 and move2 == move3 and move1 is not Move.EMPTY
    
    def get_board_grid(self):
        return self.board_grid
    
    def get_cell(self, row, col):
        return self.board_grid[row][col]
    
    def set_cell(self, row, col, move, winning_cell = False):
        self.board_grid[row][col].move = move
        self.board_grid[row][col].winning_cell = winning_cell

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

class TicTacToe(param.Parameterized):
    """
    Represents Tic Tac Toe game controller.
    This class provides methods to make moves on the board, reset game state.

    Attributes:
        first_mover (Move): Player who will make first move.
        current_move (Move): The move of the current player (either Move.X or Move.O).
        user_move_marker (Move): Move Marker selected by user.
        game_ended (bool): A flag indicating if the game has ended.
        winner (Move): The move of the winning player (either Move.X or Move.O), or Move.EMPTY if there is no winner yet.
        board (Board): Object having board 2D grid, provides methods to update game board and also provides game status.
        difficulty (Difficulty): Difficulty level selected by user.
        computer (ComputerInterface): ComputerInterface implementation object providing next move by computer. 

    Methods:
        reset_game_state(): Resets the board and game state to their initial values.
        make_move(row, col): Makes a move on the board at the specified row and column if it's a valid move.
        __update_game_state_on_move(gameState): Update game state like game_ended based on current board state. 
        __make_computer_move(): Makes a move for the computer player.
        __switch_player(): Switches the current player to the other player Eg. X to O.
        __switch_first_mover(): On every game reset, first mover is switched to add fairness to the game.
        __get_computer_move_marker(): Gives current move marker assigned to computer.
    """
    first_mover = param.Selector(objects=[Move.X, Move.O], default=Move.X)    
    current_move = param.Selector(objects=[Move.X, Move.O], default=Move.X)
    user_move_marker = param.Selector(objects=[Move.X, Move.O], default=Move.X)
    game_ended = param.Boolean(default=False)
    winner = param.Selector(objects=[Move.X, Move.O, Move.EMPTY], default=Move.EMPTY)
    board: Board = param.Parameter(Board(), instantiate=True)
    difficulty = param.ObjectSelector(default=Difficulty.EASY, objects=[Difficulty.EASY, Difficulty.INTERMEDIATE, Difficulty.PRO])
    computer: ComputerInterface = param.Parameter(BeginnerComputer(), instantiate=True)

    def reset_game_state(self):
        self.board.reset_board()
        self.computer = get_computer_by_difficulty(self.difficulty)
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
            self.game_ended = True
            self.winner = gameState[1]
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

class ViewRenderer(TicTacToe):
    """
    A class used to separate panel rendering from game logic

    Attributes:
        reset_button: Gets mapped to Button widget. Used to call reset game state in TicTacToe class

    Methods:
        reset_game_state(): Forwards request to parent game controller class to reset game state.
        game_message(): Returns the game message according to the current state of the game.
        board_view(): Returns a Panel grid representing the current state of the game board.
    """
    reset_button = param.Action(lambda x: x.param.trigger('reset_button'), label='Reset Game')

    @param.depends('reset_button','difficulty','user_move_marker', watch=True)
    def reset_game_state(self):
        '''
        Invoked when reset_button clicked or difficulty level changed or user switches their move marker. 
        Forwards request to parent class to reset game state.
        '''
        super().reset_game_state()

    @param.depends('current_move','game_ended','winner')
    def game_message(self):
        """
        Returns the game message according to the current state of the game. If the game has ended,
        the message will be whether the game ended as a draw or a winner has been declared. If the
        game is still ongoing, it will return which player's turn it is.
        Invoked when either of paramter dependecies 'current_move','game_ended','winner' are updated.
        
        Returns:
            Markdown representing the current game state message.
        """
        markdown =  pn.pane.Markdown(" ", width=GAME_MESSAGE_WIDTH)               
        if self.game_ended:
            if self.winner is not Move.EMPTY:
                if self.winner == self.user_move_marker:
                    markdown = pn.pane.Markdown(f"## You won !", width=GAME_MESSAGE_WIDTH)
                else:
                    markdown = pn.pane.Markdown(f"## Computer won :(", width=GAME_MESSAGE_WIDTH)
            else:
                markdown = pn.pane.Markdown('## Game ended as a draw', width=GAME_MESSAGE_WIDTH)
        else:
            if self.current_move == self.user_move_marker:
                markdown = pn.pane.Markdown(f"## Your turn", width=GAME_MESSAGE_WIDTH)
            else:
                markdown = pn.pane.Markdown(f"## Computer's turn", width=GAME_MESSAGE_WIDTH)
        return markdown

    @param.depends('current_move','game_ended')
    def board_view(self):
        """
        Returns a Panel grid representing the current state of the game board.
        
        This method uses the current state of the game board to generate a Panel grid
        representing the positions and values of the game buttons. Each button is associated
        with a closure that is triggered when the button is clicked, and updates the game
        state accordingly.
        
        Returns:
            A Panel GridSpec object representing the current state of the game board.
        """
        grid = pn.GridSpec(width=GRID_SIZE, height=GRID_SIZE)
        for i in range(BOARD_DIMENSION):
            for j in range(BOARD_DIMENSION):
                def make_move_closure(event, row=i, col=j):
                    self.make_move(row, col)
                button_type = 'success' if self.board.get_cell(i,j).winning_cell else 'default'   
                button = pn.widgets.Button(name=self.board.get_cell(i,j).move.value, \
                    width=GRID_BUTTON_SIZE, height=GRID_BUTTON_SIZE, button_type=button_type)
                button.param.watch(make_move_closure, 'clicks')
                grid[i, j] = button
                grid[i, j].margin = 0

        return grid

viewObj = ViewRenderer()
resetButton = pn.widgets.Button(name='Reset Game', button_type='danger')
sideViewParam = pn.Param(viewObj.param, parameters=['user_move_marker','difficulty','reset_button'], name='CONFIGURE GAME', widgets = {'reset_button': resetButton})

bootstrap = pn.template.BootstrapTemplate(title='TIC TAC TOE')
bootstrap.sidebar.append(pn.Card(sideViewParam))
bootstrap.main.append(pn.Column(viewObj.game_message, viewObj.board_view))
bootstrap.servable()

await write_doc()
  `

  try {
    const [docs_json, render_items, root_ids] = await self.pyodide.runPythonAsync(code)
    self.postMessage({
      type: 'render',
      docs_json: docs_json,
      render_items: render_items,
      root_ids: root_ids
    })
  } catch(e) {
    const traceback = `${e}`
    const tblines = traceback.split('\n')
    self.postMessage({
      type: 'status',
      msg: tblines[tblines.length-2]
    });
    throw e
  }
}

self.onmessage = async (event) => {
  const msg = event.data
  if (msg.type === 'rendered') {
    self.pyodide.runPythonAsync(`
    from panel.io.state import state
    from panel.io.pyodide import _link_docs_worker

    _link_docs_worker(state.curdoc, sendPatch, setter='js')
    `)
  } else if (msg.type === 'patch') {
    self.pyodide.runPythonAsync(`
    import json

    state.curdoc.apply_json_patch(json.loads('${msg.patch}'), setter='js')
    `)
    self.postMessage({type: 'idle'})
  } else if (msg.type === 'location') {
    self.pyodide.runPythonAsync(`
    import json
    from panel.io.state import state
    from panel.util import edit_readonly
    if state.location:
        loc_data = json.loads("""${msg.location}""")
        with edit_readonly(state.location):
            state.location.param.update({
                k: v for k, v in loc_data.items() if k in state.location.param
            })
    `)
  }
}

startApplication()