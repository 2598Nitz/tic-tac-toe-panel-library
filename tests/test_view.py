import unittest
import sys, os.path  
src_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/src/')
sys.path.append(src_path)

from model import Move
from view import ViewRenderer

class TestViewRenderer(unittest.TestCase):

    def setUp(self):
        self.view = ViewRenderer()

    def test_reset_game_state(self):
        self.view.game.first_mover = Move.O
        self.view.reset_game_state()
        self.assertEqual(self.view.game.first_mover, Move.X)

    def test_game_message(self):
        self.view.game.current_move = Move.X
        self.view.game.game_ended = False
        message = self.view.game_message().object
        self.assertIn("Your turn", message)

    def test_board_view(self):
        self.view.game.current_move = Move.X
        self.view.game.make_move(0,0)
        grid = self.view.board_view()
        button_name = grid[0, 0].name
        self.assertEqual(button_name, 'X')

if __name__ == '__main__':
    unittest.main()