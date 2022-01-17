import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


class TestColourContradiction(unittest.TestCase):
    def test_solver_clears_colour_contradiction(self):
        unsolved = " 35  6  4" \
                   " 7  54   " \
                   "4  3  5  " \
                   "6  597348" \
                   "748 63  5" \
                   "9534 8  7" \
                   "5 4  9   " \
                   "   8  45 " \
                   "3  6452  "
        edited = {
            (4, 0): {7},
            (7, 0): {2, 7},
            (7, 1): {2},
            (1, 2): {2, 8},
            (2, 2): {2},
            (4, 2): {1, 2},
            (7, 2): {1, 2, 6, 9},
            (4, 6): {7},
            (7, 6): {7},
            (1, 7): {1, 2},
            (2, 7): {1, 2},
            (4, 7): {1, 2},
            (8, 7): {1}
        }
        sudoku = Sudoku.from_string(unsolved, edited)
        solver = Solver(sudoku)

        cleared_keys = {(2, 1), (8, 1), (5, 2), (1, 3), (0, 7)}
        cleared_cells = {sudoku[key] for key in cleared_keys}
        digit = 2

        self.assertTrue(solver.check_for_two_colour_logic())
        for cell in cleared_cells:
            self.assertFalse(digit in cell)


if __name__ == '__main__':
    unittest.main()
