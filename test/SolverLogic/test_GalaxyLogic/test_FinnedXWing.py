import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


class Test_FinnedXWing(unittest.TestCase):
    unsolved = "194678   " \
               "3  512   " \
               "752394618" \
               "  52 1   " \
               "41 856  3" \
               "   9 71  " \
               "  346 7 1" \
               "   12   4" \
               " 4178359 "

    def setUp(self):
        self.sudoku = Sudoku.from_string(self.unsolved)
        self.solver = Solver(self.sudoku)
        edited = {
            (7, 0): {2},
            (0, 3): {6},
            (6, 3): {9},
            (7, 3): {7},
            (8, 3): {6},
            (0, 5): {6},
            (7, 5): {2},
            (8, 5): {2},
            (0, 6): {2, 8},
            (1, 7): {6},
            (2, 7): {6, 8}
        }
        self.sudoku.post_init(edited)

    def test_solver_clears_finned_xwings(self):
        digit = 8
        cell = self.sudoku[1, 3]

        self.assertTrue(self.solver.check_for_finned_xwings())

        self.assertFalse(digit in cell)


if __name__ == '__main__':
    unittest.main()
