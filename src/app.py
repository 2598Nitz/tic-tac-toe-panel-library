import panel as pn
from view import ViewRenderer

viewObj = ViewRenderer()
expand_layout = pn.Column()
resetButton = pn.widgets.Button(name='Reset Game', button_type='danger')
sideViewParam = pn.Param(viewObj.param, expand_button=False, expand=True, expand_layout=expand_layout, \
                         show_name=False, widgets = {'reset_button': resetButton})
bootstrap = pn.template.BootstrapTemplate(title='TIC TAC TOE')
bootstrap.sidebar.append(pn.Card(pn.Column('CONFIGURE BOARD', expand_layout, sideViewParam)))
bootstrap.main.append(pn.Column(viewObj.game_message, viewObj.board_view))
bootstrap.servable()