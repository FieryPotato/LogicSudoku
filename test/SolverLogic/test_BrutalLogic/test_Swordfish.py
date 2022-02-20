import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

COL_SWORDFISH = "7  5  894" \
                "3     527" \
                " 857 9163" \
                "9  37 4 1" \
                " 178  932" \
                "    9 7 6" \
                "   2  379" \
                "5  6  218" \
                "1 29  645"

ROW_SWORDFISH = " 29  4 68" \
                " 17682 95" \
                "68 9 3 21" \
                "9 2 6 8  " \
                "1  2486 9" \
                " 68 9 5 2" \
                "2  7 9186" \
                "   82 9  " \
                "89 4  2  "


class TestSwordfish(unittest.TestCase):
    def test_solver_clears_swordfish_in_column(self):
        sudoku = Sudoku.from_string(COL_SWORDFISH)
        solver = Solver(sudoku)
        edited = {
            (5, 0): {2},
            (1, 1): {4},
            (1, 3): {6},
            (5, 3): {5},
            (5, 5): {5},
            (0, 6): {4},
            (4, 6): {4, 8},
            (5, 6): {4, 8},
            (1, 7): {4},
            (2, 7): {4}
        }
        sudoku.post_init(edited)
        cleared_keys = {(4, 1), (5, 1), (5, 5)}
        digit = 4

        self.assertTrue(solver.check_for_fish())

        for key in cleared_keys:
            self.assertFalse(digit in sudoku[key].pencil_marks)

    def test_solver_clears_swordfish_in_row(self):
        sudoku = Sudoku.from_string(ROW_SWORDFISH)
        solver = Solver(sudoku)
        edited = {
            (1, 3): {5},
            (0, 3): {3},
            (0, 5): {3},
            (0, 7): {3, 4},
            (1, 7): {4},
            (2, 7): {3, 4, 5},
            (5, 7): {5},
            (7, 7): {7},
            (8, 7): {7},
            (2, 8): {3, 5}
        }
        sudoku.post_init(edited)
        cleared = {(4, 0), (1, 7), (4, 8)}
        digit = 5

        self.assertTrue(solver.check_for_fish())

        for key in cleared:
            self.assertFalse(digit in sudoku[key].pencil_marks)


if __name__ == '__main__':
    unittest.main()
