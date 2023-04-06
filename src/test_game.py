import unittest
from game import TicTacToe
from consts import BOARD_DIMENSION
from model import Cell, Move

class TestTicTacToe(unittest.TestCase):
    
    def setUp(self):
        self.game = TicTacToe()
        
    def test_reset_game_state(self):
        self.game.current_move = Move.O
        self.game.game_ended = True
        self.game.winner = Move.X
        self.game.reset_game_state()
        self.assertEqual(self.game.current_move, Move.X)
        self.assertEqual(self.game.game_ended, False)
        self.assertEqual(self.game.winner, Move.EMPTY)
        
    def test_make_move_accepted(self):
        self.game.make_move(0, 0)
        self.assertEqual(self.game.board[0][0].move, Move.X)
        
    def test_make_move_already_done(self):
        self.game.make_move(0, 0)
        self.game.make_move(0, 0)
        self.assertEqual(self.game.board[0][0].move, Move.X)
        
    def test_make_move_after_game_ended(self):
        self.game.board = [[Cell(move=Move.X), Cell(move=Move.EMPTY), Cell(move=Move.O)],
                           [Cell(move=Move.O), Cell(move=Move.X), Cell(move=Move.O)],
                           [Cell(move=Move.X), Cell(move=Move.O), Cell(move=Move.O)]]
        self.game.game_ended = True
        self.game.make_move(0, 1)
        self.assertEqual(self.game.board[0][1].move, Move.EMPTY)
        self.assertEqual(self.game.current_move, Move.X)
        
    def test_switch_player(self):
        self.game.current_move = Move.X
        self.game._TicTacToe__switch_player()
        self.assertEqual(self.game.current_move, Move.O)
        
    def test_get_available_moves(self):
        self.assertEqual(self.game._TicTacToe__get_available_moves(), [(i, j) for i in range(BOARD_DIMENSION) for j in range(BOARD_DIMENSION)])
        self.game.board[0][0].move = Move.X
        self.assertEqual(self.game._TicTacToe__get_available_moves(), [(i, j) for i in range(BOARD_DIMENSION) for j in range(BOARD_DIMENSION) if (i, j) != (0, 0)])
        
    def test_check_end_condition_by_moves(self):
        self.assertTrue(self.game._TicTacToe__check_end_condition_by_moves(Move.X, Move.X, Move.X))
        self.assertFalse(self.game._TicTacToe__check_end_condition_by_moves(Move.X, Move.O, Move.X))
        
if __name__ == '__main__':
    unittest.main()