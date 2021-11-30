import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

COLUMN = "  26 9175" \
         "  541   3" \
         "61 52 894" \
         "3   54   " \
         "  4 7 3  " \
         "7   6  4 " \
         " 8 2 6 31" \
         "     14  " \
         "1 67 5   "

ROW = "593   6  " \
      "7 2  39  " \
      "6 1 9  3 " \
      "2  3  465" \
      " 68574   " \
      "435   8 7" \
      "85  3   4" \
      "  6   1  " \
      "  49 7  6"


class TestSkyscraper(unittest.TestCase):
    def test_solver_clears_skyscraper_columns(self):
        sudoku = Sudoku.from_string(COLUMN)
        edited = {
            (2, 3): {9},
            (0, 4): {8},
            (2, 5): {9},
            (0, 6): {9},
            (6, 6): {9},
            (0, 7): {9},
            (1, 7): {3, 9},
            (2, 7): {7},
            (3, 7): {9},
            (4, 7): {3},
            (7, 7): {2, 8},
            (8, 7): {2, 8, 9},
            (1, 8): {2, 9},
            (4, 8): {8, 9}
        }
        sudoku.post_init(edited)
        solver = Solver(sudoku)
        cleared_keys = {(0, 4), (1, 7)}
        cleared_digit = 5

        self.assertTrue(solver.check_for_skyscraper())

        for key in cleared_keys:
            self.assertFalse(cleared_digit in sudoku[key])

    def test_solver_clears_skyscrapers_in_row(self):
        sudoku = Sudoku.from_string(ROW)
        edited = {
            (7, 0): {1, 2, 8},
            (7, 1): {1, 8},
            (6, 2): {2},
            (7, 4): {9},
            (8, 4): {1, 2},
            (7, 5): {2},
            (3, 6): {2},
            (5, 6): {2},
            (7, 6): {7},
            (7, 7): {2, 9},
            (8, 7): {2, 8},
            (4, 8): {1},
            (6, 8): {2},
            (7, 8): {2}
        }
        sudoku.post_init(edited)
        solver = Solver(sudoku)
        changed = (7, 7), (4, 8)
        digit = 5

        self.assertTrue(solver.check_for_skyscraper())

        for key in changed:
            self.assertFalse(digit in sudoku[key])


if __name__ == '__main__':
    unittest.main()
