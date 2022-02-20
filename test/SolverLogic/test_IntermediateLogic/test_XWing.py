"""
If a digit can be placed in exactly two places in two rows or columns,
pencil marks for that digit can be removed from all cells in those
columns or rows. (I.e., if a digit can be in two places in each of two
rows, and the columns for those cells line up, then cells in those
columns which are not in those rows cannot contain that digit. Likewise
for columns vis a vis rows.)
"""


import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

UNSOLVED_ROW = "8    2 3 " \
               " 24 59   " \
               "       62" \
               "   14 329" \
               " 4  27156" \
               "2 1  6   " \
               "7     2  " \
               "   2  68 " \
               " 32 8    "


UNSOLVED_COLUMN = " 9    465" \
                  "8 46   7 " \
                  "67 94  1 " \
                  "2 64  58 " \
                  "7    61 2" \
                  " 8   2  6" \
                  "   561 9 " \
                  " 6    351" \
                  "5     62 "


class TestXWing(unittest.TestCase):
    def test_solver_clears_row_x_wings(self):
        sudoku = Sudoku.from_string(UNSOLVED_ROW)
        solver = Solver(sudoku)
        keys_to_clear = {(0, 3), (3, 0), (3, 6)}
        cleared_digit = 6

        edited = {
            (6, 0): {7},
            (8, 0): {1, 7},
            (0, 1): {1},
            (3, 1): {7, 8},
            (6, 2): {7, 8},
            (3, 4): {3},
            (1, 5): {7, 8},
            (3, 5): {8},
            (6, 8): {9}
        }

        sudoku.post_init(edited)

        self.assertTrue(solver.check_for_fish())

        for key in keys_to_clear:
            self.assertFalse(cleared_digit in sudoku[key].pencil_marks)

    def test_solver_clears_column_x_wings(self):
        sudoku = Sudoku.from_string(UNSOLVED_COLUMN)
        solver = Solver(sudoku)
        keys_to_clear = {(4, 0), (4, 5), (1, 8)}
        cleared_digit = 1

        self.assertTrue(solver.check_for_fish())

        for key in keys_to_clear:
            self.assertFalse(cleared_digit in sudoku[key].pencil_marks)


if __name__ == '__main__':
    unittest.main()
