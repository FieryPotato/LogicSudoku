import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


class TestEmptyRectangleFunctions(unittest.TestCase):
    def setUp(self) -> None:
        unsolved = "  857 6 4" \
                   "46   2 75" \
                   "5 74   3 " \
                   "94 1   8 " \
                   "   8 5   " \
                   " 8 2    1" \
                   " 5 6 4  7" \
                   "8 475  26" \
                   "176 2 45 "
        self.sudoku = Sudoku.from_string(unsolved)
        edited = {
            (1, 0): {9},
            (6, 1): {9},
            (1, 2): {2},
            (4, 2): {8},
            (6, 2): {8},
            (6, 3): {3},
            (0, 4): {2, 3},
            (4, 4): {6},
            (7, 4): {9},
            (0, 5): {3},
            (4, 5): {6},
            (5, 5): {6},
            (7, 5): {9},
            (4, 6): {9}
        }
        self.sudoku.post_init(edited)
        self.solver = Solver(self.sudoku)

    def test_box_contains_filled_digit(self):
        self.assertFalse(self.sudoku.box_contains_filled_digit(0, 1))
        self.assertTrue(self.sudoku.box_contains_filled_digit(5, 8))


if __name__ == '__main__':
    unittest.main()
