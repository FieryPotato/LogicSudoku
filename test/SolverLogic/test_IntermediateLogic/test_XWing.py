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


class TestXWing(unittest.TestCase):
    def test_solver_clears_cells_in_columns(self):
        sudoku = Sudoku.from_string(UNSOLVED_ROW)
        solver = Solver(sudoku)
        keys_to_clear = {(0, 3), (3, 0), (3, 6)}
        cleared_digit = 6

        self.assertTrue(solver.check_for_xwings())

        for key in keys_to_clear:
            self.assertFalse(cleared_digit in sudoku[key].pencil_marks)


if __name__ == '__main__':
    unittest.main()
