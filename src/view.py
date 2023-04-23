from game import TicTacToe
import param
from model import Move
from consts import BOARD_DIMENSION,GRID_SIZE,GRID_BUTTON_SIZE,GAME_MESSAGE_WIDTH
import panel as pn

class ViewRenderer(param.Parameterized):
    """
    A class used to separate panel rendering from game logic

    Methods:
        reset_game_state(): Forwards request to parent game controller class to reset game state.
        game_message(): Returns the game message according to the current state of the game.
        board_view(): Returns a Panel grid representing the current state of the game board.
    """
    reset_button = param.Action(lambda x: x.param.trigger('reset_button'), label='Reset Game', \
                                doc='Gets mapped to Button widget. Used to call reset game state in TicTacToe class')
    game = param.ClassSelector(class_=TicTacToe, default=TicTacToe(), precedence=-1, doc='Game logic containing object')

    def __init__(self, **params):
        '''
        Initialize GridSpec with button widgets for Tic Tac Toe board.
        Button widget are being listened for clicks and game state is updated on click.
        '''
        super(ViewRenderer, self).__init__(**params)
        self.grid = pn.GridSpec(width=GRID_SIZE, height=GRID_SIZE)
        for i in range(BOARD_DIMENSION):
            for j in range(BOARD_DIMENSION):
                def make_move_closure(event, row=i, col=j):
                    self.game.make_move(row, col) 
                button = pn.widgets.Button(name=Move.EMPTY.value, width=GRID_BUTTON_SIZE, height=GRID_BUTTON_SIZE)
                button.param.watch(make_move_closure, 'clicks')
                self.grid[i, j] = button
                self.grid[i, j].margin = 0  

    @param.depends('reset_button','game.difficulty','game.user_move_marker', watch=True)
    def reset_game_state(self):
        '''
        Invoked when reset_button clicked or difficulty level changed or user switches their move marker. 
        Forwards request to parent class to reset game state.
        '''
        self.game.reset_game_state()

    @param.depends('game.current_move','game.game_ended','game.winner')
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
        if self.game.game_ended:
            if self.game.winner is not Move.EMPTY:
                if self.game.winner == self.game.user_move_marker:
                    markdown.object = "## You won !"
                else:
                    markdown.object = "## Computer won :("
            else:
                markdown.object = '## Game ended as a draw'
        else:
            if self.game.current_move == self.game.user_move_marker:
                markdown.object = "## Your turn"
            else:
                markdown.object = "## Computer's turn"
        return markdown

    @param.depends('game.current_move','game.game_ended')
    def board_view(self):
        """
        Returns a Panel grid representing the current state of the game board.
        
        This method uses the current state of the game board to update Panel grid
        representing the positions and values of the game buttons. 
        
        Returns:
            A Panel GridSpec object representing the current state of the game board.
        """

        for i in range(BOARD_DIMENSION):
            for j in range(BOARD_DIMENSION):
                self.grid[i, j].name = self.game.board.get_cell(i,j).move.value
                self.grid[i, j].button_type = 'success' if self.game.board.get_cell(i,j).winning_cell else 'default'
        return self.grid    