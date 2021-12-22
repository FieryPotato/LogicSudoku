"""

"""

import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


HIDDEN_ROW = "8394 6   " \
             "16   3   " \
             "25   16  " \
             "9   6 3  " \
             " 137 98 6" \
             "    3 9 4" \
             "   3 7195" \
             "3   1 267" \
             "  16 24  "

HIDDEN_COL = "2467591  " \
             "    64527" \
             "    23469" \
             "  459   2" \
             "192376854" \
             " 7 4 239 " \
             "46 23    " \
             "8 194    " \
             "   6   45"

HIDDEN_BOX = "36   2 4 " \
             "7 4 3    " \
             "829764351" \
             "596247183" \
             "432158   " \
             "187396524" \
             "243  961 " \
             "9786  43 " \
             "6  4 3  8"


class TestHiddenRectangle(unittest.TestCase):
    def test_solver_clears_hidden_rectangle_in_rows(self):
        sudoku = Sudoku.from_string(HIDDEN_ROW)
        changed_keys = {(7, 2), (8, 2)}
        removed_digit = 8
        edited = {
            (0, 0): {},
            (1, 0): {},
            (4, 0): {2},
            (7, 0): {5, 7},
            (4, 1): {5, 7},
            (7, 1): {2, 5, 7},
            (8, 1): {2},
            (6, 2): {},
            (7, 2): {7},
            (2, 3): {4, 7},
            (3, 3): {5},
            (6, 3): {},
            (7, 3): {1, 2},
            (1, 4): {},
            (4, 4): {5},
            (8, 4): {},
            (2, 5): {7},
            (3, 5): {5},
            (6, 5): {},
            (1, 6): {4},
            (2, 6): {4},
            (5, 6): {},
            (6, 6): {},
            (2, 7): {4},
            (3, 7): {8},
            (5, 7): {5},
            (6, 7): {},
            (1, 8): {8},
            (2, 8): {},
            (3, 8): {},
            (4, 8): {8}
        }
        sudoku.post_init(edited)

        solver = Solver(sudoku)

        self.assertTrue(solver.check_for_hidden_rectangle())

        for key in changed_keys:
            self.assertFalse(removed_digit in sudoku[key].pencil_marks)

    def test_solver_clears_hidden_rectangle_in_columns(self):
        sudoku = Sudoku.from_string(HIDDEN_COL)
        changed_keys = {(1, 1), (1, 2)}
        removed_digit = 8
        edited = {
            (1, 0): set(),
            (2, 0): set(),
            (3, 0): set(),
            (4, 0): set(),
            (5, 0): set(),
            (6, 0): set(),
            (6, 1): set(),
            (4, 2): set(),
            (5, 2): set(),
            (0, 4): set(),
            (2, 4): set(),
            (6, 4): set(),
            (7, 4): set(),
            (8, 4): set(),
            (3, 5): set(),
            (7, 5): set(),
            (3, 6): set(),
            (4, 6): set(),
            (5, 6): {1, 8},
            (7, 6): {7},
            (1, 7): {3},
            (3, 8): set(),
            (5, 8): {7},
            (7, 8): set()
        }
        sudoku.post_init(edited)

        solver = Solver(sudoku)

        self.assertTrue(solver.check_for_hidden_rectangle())

        for key in changed_keys:
            self.assertFalse(removed_digit in sudoku[key].pencil_marks)

    def test_solver_clears_hidden_rectangle_opposite(self):
        sudoku = Sudoku.from_string(HIDDEN_BOX)
        solver = Solver(sudoku)
        edited = {
            (7, 0): {},
            (0, 1): {},
            (3, 1): {5},
            (4, 1): {},
            (0, 2): {},
            (1, 2): {},
            (4, 2): {},
            (5, 2): {},
            (7, 2): {},
            (2, 3): {},
            (3, 3): {},
            (5, 3): {},
            (6, 3): {},
            (7, 3): {},
            (8, 3): {},
            (0, 4): {},
            (1, 4): {},
            (2, 4): {},
            (4, 4): {},
            (0, 5): {},
            (1, 5): {},
            (2, 5): {},
            (3, 5): {},
            (6, 5): {},
            (1, 6): {},
            (7, 6): {},
            (0, 7): {},
            (2, 7): {},
            (3, 7): {},
            (6, 7): {},
            (7, 7): {},
            (0, 8): {},
            (5, 8): {}
        }
        sudoku.post_init(edited)
        changed = sudoku[8, 4]
        digit = 9

        self.assertTrue(solver.check_for_hidden_rectangle())

        self.assertFalse(digit in changed.pencil_marks)


if __name__ == '__main__':
    unittest.main()
