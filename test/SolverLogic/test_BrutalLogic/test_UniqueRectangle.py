import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

UNSOLVED = "46 7 8 3 " \
           " 7  93468" \
           "38 4   7 " \
           "   83 695" \
           "   95 723" \
           "593  7814" \
           "    49 87" \
           "   172 56" \
           "   38  42"


class TestUniqueRectangle(unittest.TestCase):
    def test_solver_fills_unique_rectangle(self):
        sudoku = Sudoku.from_string(UNSOLVED)
        solver = Solver(sudoku)
        changed_key = (1, 3)
        digits_to_remove = {1, 4}

        edited = {
            (2, 0): {1},
            (6, 0): {1, 9},
            (2, 2): {1},
            (5, 2): {1, 4},
            (6, 2): {1, 9},
            (5, 3): {2, 3, 5, 6, 7, 8, 9},
            (5, 4): {2, 3, 5, 6, 7, 8, 9},
            (3, 5): {1, 4},
            (4, 5): {1, 4},
            (2, 6): {5},
            (2, 7): {9},
            (2, 8): {5, 9},
            (5, 8): {1, 4}
        }

        sudoku.post_init(edited)

        self.assertTrue(solver.check_for_unique_rectangle())

        for digit in digits_to_remove:
            self.assertFalse(digit in sudoku[changed_key].pencil_marks)


if __name__ == '__main__':
    unittest.main()
