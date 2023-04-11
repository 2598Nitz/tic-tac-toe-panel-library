import unittest
import sys, os.path  
src_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/src/')
sys.path.append(src_path)

from game import TicTacToe
from model import Cell, Move
from board import Board

class TestTicTacToe(unittest.TestCase):
    
    def setUp(self):
        self.game = TicTacToe()
        
    def test_reset_game_state(self):
        self.game.current_move = Move.O
        self.game.game_ended = True
        self.game.board.set_cell(0,1,Move.X)
        self.game.winner = Move.X
        self.game.reset_game_state()
        self.assertEqual(self.game.current_move, Move.X)
        self.assertEqual(self.game.board.get_cell(0,1).move, Move.EMPTY)
        self.assertEqual(self.game.game_ended, False)
        self.assertEqual(self.game.winner, Move.EMPTY)
        
    def test_make_move_accepted(self):
        self.game.make_move(0, 0)
        self.assertEqual(self.game.board.get_cell(0,0).move, Move.X)
        
    def test_make_move_already_done(self):
        self.game.make_move(0, 0)
        self.game.current_move = Move.O
        self.game.make_move(0, 0)
        self.assertEqual(self.game.board.get_cell(0,0).move, Move.X)
        
    def test_make_move_after_game_ended(self):
        board_grid = [[Cell(move=Move.X), Cell(move=Move.EMPTY), Cell(move=Move.O)],
                           [Cell(move=Move.O), Cell(move=Move.X), Cell(move=Move.O)],
                           [Cell(move=Move.X), Cell(move=Move.O), Cell(move=Move.O)]]
        self.board = Board(board_grid)
        self.game.game_ended = True
        self.game.make_move(0, 1)
        self.assertEqual(self.game.board.get_cell(0,1).move, Move.EMPTY)
        self.assertEqual(self.game.current_move, Move.X)
        
if __name__ == '__main__':
    unittest.main()