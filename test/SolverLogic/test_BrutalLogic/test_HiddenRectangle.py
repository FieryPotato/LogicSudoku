import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


UNSOLVED_1 = "281437659" \
             "      217" \
             "759216   " \
             "       7 " \
             " 978 5   " \
             " 25 739  " \
             "5  79 3  " \
             "3    479 " \
             "974362 8 "


UNSOLVED_2 = "2467591  " \
             "    64527" \
             "    23469" \
             "  459   2" \
             "192376854" \
             " 7 4 239 " \
             "46 23    " \
             "8 194    " \
             "   6   45"


class TestHiddenRectangle(unittest.TestCase):
    def test_solver_clears_hidden_rectangle_in_columns(self):
        sudoku = Sudoku.from_string(UNSOLVED_1)
        changed_keys = {(6, 3), (8, 3)}
        removed_digit = 1
        edited = {
            (0, 0): set(),
            (2, 0): set(),
            (3, 0): set(),
            (4, 0): set(),
            (6, 0): set(),
            (8, 0): set(),
            (1, 1): {6},
            (0, 2): set(),
            (1, 2): set(),
            (3, 2): set(),
            (5, 2): set(),
            (1, 3): {1, 6},
            (2, 3): {8},
            (8, 3): {3},
            (1, 4): set(),
            (2, 4): set(),
            (4, 5): set(),
            (5, 5): set(),
            (8, 5): {1},
            (0, 6): set(),
            (2, 6): {6},
            (3, 6): set(),
            (8, 6): {1},
            (6, 7): set(),
            (7, 7): set(),
            (8, 7): {1, 5},
            (0, 8): set(),
            (2, 8): set(),
            (4, 8): set()
        }
        sudoku.post_init(edited)

        solver = Solver(sudoku)

        self.assertTrue(solver.check_for_hidden_rectangle())

        for key in changed_keys:
            self.assertFalse(removed_digit in sudoku[key].pencil_marks)

    def test_solver_clears_hidden_rectangle_in_rows(self):
        sudoku = Sudoku.from_string(UNSOLVED_2)
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

if __name__ == '__main__':
    unittest.main()
