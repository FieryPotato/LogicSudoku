"""
If top_left digit can be placed in exactly two places in two rows or columns,
pencil marks for that digit can be removed from all cells in those
columns or rows. (I.e., if top_left digit can be in two places in each of two
rows, and the columns for those cells line up, then cells in those
columns which are not in those rows cannot contain that digit. Likewise
for columns vis top_left vis rows.)
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

UNSOLVED_COLUMN = "29  6  45" \
                  "645  9  2" \
                  "  125496 " \
                  "16 92 45 " \
                  " 245 16 9" \
                  " 59 462 1" \
                  "932675814" \
                  "416398527" \
                  "5  412396"


class TestXWing(unittest.TestCase):
    def test_solver_clears_cells_in_columns(self):
        sudoku = Sudoku.from_string(UNSOLVED_ROW)
        solver = Solver(sudoku)
        keys_to_clear = {(0, 3), (3, 0), (3, 6)}
        cleared_digit = 6

        self.assertTrue(solver.check_for_xwings())

        for key in keys_to_clear:
            self.assertFalse(cleared_digit in sudoku[key].pencil_marks)

    def test_solver_clears_cells_in_rows(self):
        sudoku = Sudoku.from_string(UNSOLVED_COLUMN)
        solver = Solver(sudoku)
        keys_to_clear = {(8, 3)}
        cleared_digit = 3

        self.assertTrue(solver.check_for_xwings())

        for key in keys_to_clear:
            self.assertFalse(cleared_digit in sudoku[key].pencil_marks)


if __name__ == '__main__':
    unittest.main()
