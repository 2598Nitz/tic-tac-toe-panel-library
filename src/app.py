import panel as pn
from view import ViewRenderer

viewObj = ViewRenderer()
pn.Column(viewObj.game_message, viewObj.board_view, pn.panel(viewObj.param, parameters=['reset_button'], name='')).servable()