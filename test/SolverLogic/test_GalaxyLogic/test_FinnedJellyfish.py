import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


class TestFinnedJellyfishRow(unittest.TestCase):
    def setUp(self):
        unsolved = "415  7 96" \
                   "9  61 745" \
                   "6    518 " \
                   "1   7 86 " \
                   "8  3 6  1" \
                   "  6128  9" \
                   "   76 91 " \
                   "769  1  8" \
                   "  1   657"
        edited = {
            (3, 2): {2},
            (4, 2): {3},
            (1, 3): {4},
            (1, 6): {2, 4},
            (2, 6): {2},
            (1, 8): {2, 8}
        }
        self.sudoku = Sudoku.from_string(unsolved, edited)
        self.solver = Solver(self.sudoku)

    def test_solver_clears_row_finned_jellyfish(self):
        affected = self.sudoku[1, 8]
        digit = 3

        self.assertTrue(self.solver.check_for_fish())
        self.assertFalse(digit in affected)


class TestFinnedJellyfishColumn(unittest.TestCase):
    def setUp(self) -> None:
        unsolved = "1 2   93 " \
                   " 45    81" \
                   " 831 74  " \
                   "5 9   643" \
                   "  45368 9" \
                   "836      " \
                   "3 74 1568" \
                   " 58   194" \
                   "4 1   372"
        edited = {
            (3, 1): {2},
            (1, 3): {7},
            (3, 5): {7},
            (4, 5): {2, 7},
        }
        self.sudoku = Sudoku.from_string(unsolved, edited)
        self.solver = Solver(self.sudoku)

    def test_solver_clears_column_finned_jellyfish(self):
        digit = 2
        cell = self.sudoku[1, 3]
        self.assertTrue(self.solver.check_for_fish())
        self.assertFalse(digit in cell)


if __name__ == "__main__":
    unittest.main()