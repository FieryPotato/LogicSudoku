import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


UNSOLVED = "   39 486" \
             "8 367 912" \
             " 96 28537" \
             "687 4 359" \
             "9  783621" \
             "231569874" \
             "   9  76 " \
             "56  17293" \
             "  9  614 "


class TestXYZWings(unittest.TestCase):
    def test_solver_clears_xyzwings(self):
        sudoku = Sudoku.from_string(UNSOLVED)
        edited = {
            (1, 0): {5},
            (1, 6): {4},
            (5, 6): {5}
        }
        sudoku.post_init(edited)
        solver = Solver(sudoku)
        affected = sudoku[(0, 6)]
        digit_to_remove = 4

        self.assertTrue(solver.check_for_xyzwings())

        self.assertFalse(digit_to_remove in affected.pencil_marks)


if __name__ == "__main__":
    unittest.main()
