from game import TicTacToe
import param
from model import Move
from consts import BOARD_DIMENSION,GRID_SIZE,GRID_BUTTON_SIZE
import panel as pn

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
                return f"Winner is {self.winner.value}"
            else:
                return 'Game ended as a draw'
        else:
            return f"Player {self.current_move.value}'s turn"

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
        return grid