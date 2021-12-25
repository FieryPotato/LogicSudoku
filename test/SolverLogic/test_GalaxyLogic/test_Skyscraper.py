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

ROW = " 84  61 9" \
      " 69  1 8 " \
      "5139 87 6" \
      "625793418" \
      " 7816 9  " \
      " 918   67" \
      "  26    1" \
      "  7   69 " \
      "  65  8  "


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

    def test_solver_clears_skyscraper_in_columns(self):
        sudoku = Sudoku.from_string(ROW)
        edited = {
            (4, 0): {2, 3},
            (7, 0): {2},
            (4, 1): {2, 3, 4},
            (7, 4): {2},
            (4, 5): {5},
            (0, 6): {3, 4},
            (4, 6): {4, 7},
            (5, 6): {4},
            (7, 6): {3, 5},
            (0, 7): {3, 4},
            (1, 7): {4},
            (3, 7): {3},
            (4, 7): {2, 3, 4},
            (8, 7): {2, 4},
            (0, 8): {3, 4},
            (4, 8): {2, 4, 7},
            (5, 8): {2, 4},
            (7, 8): {3},
            (8, 8): {3}
        }
        sudoku.post_init(edited)




if __name__ == '__main__':
    unittest.main()
