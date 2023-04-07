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
  const env_spec = ['https://cdn.holoviz.org/panel/0.14.4/dist/wheels/bokeh-2.4.3-py3-none-any.whl', 'https://cdn.holoviz.org/panel/0.14.4/dist/wheels/panel-0.14.4-py3-none-any.whl', 'pyodide-http==0.1.0', 'param']
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

import panel as pn
import param
import random
import time

from enum import Enum

class Move(Enum):
    EMPTY = ' '
    X = 'X'
    O = 'O'

class Cell(param.Parameterized):
    winning_cell = param.Boolean(default=False)
    move = param.ClassSelector(class_=Move, default=Move.EMPTY)

BOARD_DIMENSION = 3
GRID_SIZE = 300
GRID_BUTTON_SIZE = 100
COMPUTER_DELAY_SEC = 0.5

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
    
class ViewRenderer(TicTacToe):
    """
    A class used to separate panel rendering from game logic

    ...

    Attributes
    ----------
    reset_button : Action
        Gets mapped to Button widget. Used to call reset game state in TicTacToe class

    Methods
    -------
    reset_game_state()
        Forwards request to parent class to reset game state

    game_message()
        Returns the game message according to the current state of the game.

    board_view()
        Returns a Panel grid representing the current state of the game board.
    """
    reset_button = param.Action(lambda x: x.param.trigger('reset_button'), label='Reset Game')

    @param.depends('reset_button', watch=True)
    def reset_game_state(self):
        '''Invoked when reset_button clicked. Forwards request to parent class to reset game state.'''
        super().reset_game_state()

    @param.depends('current_move','game_ended','winner')
    def game_message(self):
        """
        Returns the game message according to the current state of the game. If the game has ended,
        the message will be whether the game ended as a draw or a winner has been declared. If the
        game is still ongoing, it will return which player's turn it is.
        Invoked when either of paramter dependecies 'current_move','game_ended','winner' are updated.
        
        Returns:
        str: A string representing the current game state message.
        """                
        if self.game_ended:
            if self.winner is not Move.EMPTY:
                return f"# Winner is Player {self.winner.value}"
            else:
                return '# Game ended as a draw'
        else:
            return f"# Player {self.current_move.value}'s turn"

    @param.depends('current_move')
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
                button_type = 'success' if self.board[i][j].winning_cell else 'default'    
                button = pn.widgets.Button(name=self.board[i][j].move.value, \
                    width=GRID_BUTTON_SIZE, height=GRID_BUTTON_SIZE, button_type=button_type)
                button.param.watch(make_move_closure, 'clicks')
                grid[i, j] = button
                grid[i, j].margin = 0
        grid.margin = (0, 0, 20, 0) #left aligned
        return grid

viewObj = ViewRenderer()
resetButton = pn.widgets.Button(name='Reset Game', button_type='danger', width = GRID_SIZE)
resetButton.margin = 0 #left aligned
resetButtonParam = pn.Param(viewObj.param, parameters=['reset_button'], name='', widgets = {'reset_button': resetButton})
pn.Column(viewObj.game_message, viewObj.board_view, resetButton).servable()

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