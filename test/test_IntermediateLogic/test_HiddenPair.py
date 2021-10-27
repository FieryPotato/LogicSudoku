import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

UNSOLVED_BOX = "6  1  27 " \
               "   9  6  " \
               "3  276  4" \
               "  6 3  25" \
               "  9 683  " \
               "73  2  6 " \
               "5  61  32" \
               " 638 2   " \
               " 1 3    6"


class TestHiddenPair(unittest.TestCase):
    def test_solver_clears_pencil_marks_in_box(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_BOX)
        solver: Solver = Solver(sudoku)
        hidden_pair: tuple = ((5, 3), (5, 5))

        solver.check_for_hidden_pairs()

        for key in hidden_pair:
            pencil_marks = sudoku[key].pencil_marks
            self.assertTrue(1 in pencil_marks and 9 in pencil_marks and len(pencil_marks) == 2)


if __name__ == '__main__':
    unittest.main()
