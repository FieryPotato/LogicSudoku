import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

UNSOLVED_BOX: str = " 91      " \
                    " 3 8 9 2 " \
                    " 2  5  9 " \
                    "6 3 98 7 " \
                    "   2 7   " \
                    " 8  6 4  " \
                    " 6 38  4 " \
                    "31   6 8 " \
                    " 7    653"


class TestNakedPair(unittest.TestCase):
    def test_solver_clears_pencil_marks_for_naked_pairs_in_box(self):
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_BOX)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((0, 4), (0, 5), (2, 4), (2, 5))
        naked_pair: tuple = ((1, 3), (1, 4))

        solver.check_for_naked_pairs()

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            self.assertFalse(4 in pencil_marks or 5 in pencil_marks)
        for key in naked_pair:
            pencil_marks = sudoku[key].pencil_marks
            self.assertTrue(4 in pencil_marks and 5 in pencil_marks)


if __name__ == '__main__':
    unittest.main()
