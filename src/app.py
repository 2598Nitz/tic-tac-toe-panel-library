import panel as pn
from view import ViewRenderer
from consts import GRID_SIZE

viewObj = ViewRenderer()
resetButton = pn.widgets.Button(name='Reset Game', button_type='danger', width = GRID_SIZE)
resetButton.margin = 0 #left aligned
resetButtonParam = pn.Param(viewObj.param, parameters=['reset_button'], name='', widgets = {'reset_button': resetButton})
pn.Column(viewObj.game_message, viewObj.board_view, resetButton).servable()