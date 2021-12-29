import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


class TestFinnedSwordfishRow(unittest.TestCase):
    def setUp(self):
        unsolved = "1    2   " \
                   " 7  13 65" \
                   " 634 78 1" \
                   "397248516" \
                   "625 31 48" \
                   "8145 6   " \
                   "732189654" \
                   "9 63  18 " \
                   " 81     3"
        edited = {
            (3, 0): {9},
            (6, 1): {9},
            (4, 7): {5},
            (4, 8): {5},
            (7, 8): {2}
        }
        self.sudoku = Sudoku.from_string(unsolved, edited)
        self.solver = Solver(self.sudoku)

    def test_solver_clears_finned_swordfish(self):
        digit = 9
        affected = self.sudoku[6, 4]
        self.assertTrue(self.solver.check_for_fish())
        self.assertFalse(digit in affected)


if __name__ == '__main__':
    unittest.main()
