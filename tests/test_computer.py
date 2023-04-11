import unittest
import sys, os.path  
src_path = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/src/')
sys.path.append(src_path)

from model import Cell,Move
from board import Board
from computer import get_best_move, get_non_best_move, BeginnerComputer

class TestComputer(unittest.TestCase):

    def test_get_best_move(self):
        board_grid = [[Cell(move=Move.X), Cell(move=Move.EMPTY), Cell(move=Move.O)],
                           [Cell(move=Move.O), Cell(move=Move.X), Cell(move=Move.O)],
                           [Cell(move=Move.EMPTY), Cell(move=Move.O), Cell(move=Move.EMPTY)]] 
        board = Board(board_grid)
        available_moves = [(0,1),(2,0),(2,2)]
        best_move = get_best_move(available_moves, board, Move.O)
        self.assertEqual(best_move, (2,2))

    def test_get_non_best_move(self):
        board_grid = [[Cell(move=Move.X), Cell(move=Move.EMPTY), Cell(move=Move.O)],
                           [Cell(move=Move.O), Cell(move=Move.X), Cell(move=Move.O)],
                           [Cell(move=Move.X), Cell(move=Move.O), Cell(move=Move.EMPTY)]] 
        board = Board(board_grid)
        available_moves = [(0,1),(2,2)]
        best_move = get_best_move(available_moves, board, Move.O)
        non_best_move = get_non_best_move(available_moves, best_move)
        self.assertEqual(non_best_move, (0,1))

    def test_random_move(self):
        board = Board()
        board.set_cell(0,0,Move.X)
        computer = BeginnerComputer()
        move = computer.get_move(board, Move.O)
        self.assertTrue(move != None)
        self.assertNotEqual(move, (0,0))
           

if __name__ == '__main__':
    unittest.main()