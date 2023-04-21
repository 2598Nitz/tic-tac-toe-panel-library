import panel as pn
from view import ViewRenderer

viewObj = ViewRenderer()
resetButton = pn.widgets.Button(name='Reset Game', button_type='danger')
sideViewParam = pn.Param(viewObj.param, parameters=['user_move_marker','difficulty','reset_button'], name='CONFIGURE GAME', widgets = {'reset_button': resetButton})

bootstrap = pn.template.BootstrapTemplate(title='TIC TAC TOE')
bootstrap.sidebar.append(pn.Card(sideViewParam))
bootstrap.main.append(pn.Column(viewObj.game_message, viewObj.board_view))
bootstrap.servable()