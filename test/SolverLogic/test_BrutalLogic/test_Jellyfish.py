import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


ROW_JELLYFISH = " 3 8 5 7 " \
                "  8 79  3" \
                "7  34 2 8" \
                " 73  49 5" \
                "9  53 4 7" \
                "  279 3 1" \
                "6 59837 2" \
                "3  65 8  " \
                "   4  536"

COL_JELLYFISH = "1  742 3 " \
                "7 5      " \
                " 3 6  7  " \
                "  7    1 " \
                "84 1 9 73" \
                " 1  7 9  " \
                "     734 " \
                "    3 2 7" \
                " 7 48  96"


class TestJellyfish(unittest.TestCase):
    def test_solver_clears_jellyfish_in_row(self):
        sudoku = Sudoku.from_string(ROW_JELLYFISH)
        solver = Solver(sudoku)
        edited = {
            (0, 0): {4},
            (2, 0): {1, 6},
            (0, 1): {1, 2},
            (1, 1): {4, 5},
            (7, 1): {1, 6},
            (7, 2): {1, 6},
            (7, 4): {6},
            (0, 5): {8},
            (1, 5): {6, 8},
            (1, 7): {4, 9},
            (2, 7): {9},
            (7, 7): {4},
        }
        sudoku.post_init(edited)
        changed = {(1, 1), (1, 8), (2, 8), (5, 8)}
        digit = 1

        self.assertTrue(solver.check_for_fish())

        for key in changed:
            self.assertFalse(digit in sudoku[key].pencil_marks)

    def test_solver_clears_jellyfish_in_column(self):
        sudoku = Sudoku.from_string(COL_JELLYFISH)
        solver = Solver(sudoku)
        edited = {
            (2, 0): {6},
            (2, 2): {2},
            (7, 2): {5},
            (8, 2): {4, 5},
            (0, 3): {6},
            (1, 3): {6},
            (5, 3): {5},
            (0, 5): {6},
            (5, 5): {5},
            (0, 6): {2},
            (1, 6): {2, 6},
            (2, 6): {2, 6},
            (4, 6): {5},
            (0, 7): {5, 9},
            (1, 7): {6},
            (2, 7): {6, 8, 9},
            (5, 7): {5},
            (0, 8): {5},
            (2, 8): {1}
        }
        changed = {(4, 3), (8, 3), (8, 5), (8, 6)}
        digit = 5

        self.assertTrue(solver.check_for_fish())

        for key in changed:
            self.assertFalse(digit in sudoku[key].pencil_marks)


if __name__ == '__main__':
    unittest.main()
