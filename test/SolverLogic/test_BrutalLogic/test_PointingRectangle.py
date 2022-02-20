import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

UNSOLVED_SAME = "92 743   " \
                "65 129   " \
                " 7 5682  " \
                "837914 2 " \
                "265387   " \
                "149256387" \
                "  2 3 8  " \
                "  687  32" \
                " 8  92 51"

UNSOLVED_CROSS = "67 3 5   " \
                 "   67 485" \
                 "5     673" \
                 " 4  9  5 " \
                 "   4 6   " \
                 "   852 4 " \
                 "83     64" \
                 "42  68 3 " \
                 "1  9  827"


class TestPointingRectangle(unittest.TestCase):
    def test_solver_clears_pointing_rectangle_with_pair_in_same_box(self):
        sudoku = Sudoku.from_string(UNSOLVED_SAME)
        solver = Solver(sudoku)

        edited = {
            (3, 0): set(),
            (5, 0): set(),
            (7, 0): {1},
            (0, 1): set(),
            (2, 1): {4},
            (4, 1): set(),
            (5, 1): set(),
            (8, 1): {4},
            (1, 2): set(),
            (3, 2): set(),
            (4, 2): set(),
            (7, 2): {4},
            (8, 2): {4},
            (2, 3): set(),
            (4, 3): set(),
            (5, 3): set(),
            (7, 3): set(),
            (0, 4): set(),
            (1, 4): set(),
            (2, 4): set(),
            (0, 5): set(),
            (2, 5): set(),
            (3, 5): set(),
            (4, 5): set(),
            (6, 5): set(),
            (7, 5): set(),
            (4, 6): set(),
            (7, 6): {4},
            (3, 7): set(),
            (4, 7): set(),
            (8, 7): set(),
            (5, 8): set()
        }

        sudoku.post_init(edited)

        affected_key = (7, 0)
        digits = {1, 8}

        self.assertTrue(solver.check_for_pointing_rectangle())

        for digit in digits:
            self.assertFalse(digit in sudoku[affected_key].pencil_marks)

    def test_solver_clears_pointing_rectangle_with_pair_in_two_boxes(self):
        sudoku = Sudoku.from_string(UNSOLVED_CROSS)
        solver = Solver(sudoku)

        edited = {
            (1, 0): set(),
            (2, 0): {1, 2, 9},
            (3, 0): set(),
            (4, 0): {1, 2},
            (0, 1): {9},
            (2, 1): {1, 9},
            (3, 1): set(),
            (8, 1): set(),
            (2, 2): {2, 9},
            (6, 2): set(),
            (0, 3): {7},
            (2, 3): {1, 2, 3, 7},
            (6, 3): {7},
            (7, 3): set(),
            (8, 3): {1, 2},
            (0, 4): {2, 3},
            (1, 4): {9},
            (2, 4): {7, 9},
            (0, 5): {3},
            (1, 5): {9},
            (2, 5): {7, 9},
            (6, 5): {1},
            (2, 6): {5},
            (7, 6): set(),
            (8, 6): set(),
            (2, 7): {5},
            (5, 7): set(),
            (0, 8): set(),
            (6, 8): set(),
            (7, 8): set()
        }

        sudoku.post_init(edited)

        affected_keys = {(1, 2), (5, 2)}
        digits = {1, 2}

        self.assertTrue(solver.check_for_pointing_rectangle())

        for key in affected_keys:
            for digit in digits:
                self.assertFalse(digit in sudoku[key].pencil_marks)


if __name__ == '__main__':
    unittest.main()
