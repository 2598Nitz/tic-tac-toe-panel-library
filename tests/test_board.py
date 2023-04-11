import unittest
import sys, os.path  
src_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/src/')
sys.path.append(src_path)

from board import Board
from model import Move,GameStatus

class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_board_initialization_with_copy_constructor(self):
        self.board.set_cell(0,0,Move.X)
        new_board = Board(self.board.get_board_grid())
        self.assertFalse(self.board.get_cell(0,0) == new_board.get_board_grid()[0][0])
        self.assertTrue(self.board.get_cell(0,0).move == new_board.get_board_grid()[0][0].move)

    def test_reset_board(self):
        self.board.set_cell(0,0,Move.X)
        self.board.reset_board()
        self.assertTrue(self.board.get_cell(0,0).move == Move.EMPTY)

    def test_get_available_moves(self):
        self.board.set_cell(0,0,Move.X)
        self.board.set_cell(0,1,Move.O)
        self.assertEqual(len(self.board.get_available_moves()), 7)

    def test_game_winning_state(self):
        self.board.set_cell(0,0,Move.X)
        self.board.set_cell(1,1,Move.X)
        self.board.set_cell(2,2,Move.X)
        self.board.set_cell(0,1,Move.O)
        self.board.set_cell(0,2,Move.O)
        game_state = self.board.get_game_state()
        self.assertEqual(game_state[0], GameStatus.WIN)
        self.assertEqual(game_state[1], Move.X)
        self.assertEqual(game_state[2], ((0,0), (1,1), (2,2),))

    def test_get_set_cell(self):
        self.board.set_cell(0,0,Move.X)
        self.assertTrue(self.board.get_cell(0,0).move == Move.X)        

if __name__ == '__main__':
    unittest.main()