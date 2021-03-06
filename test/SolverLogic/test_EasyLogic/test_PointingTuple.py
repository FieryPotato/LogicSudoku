"""
If a digit's possible positions in a box all occur in the same row or
column, that digit can be eliminated from pencil marks of all other
cells in that row or column.
"""


import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

UNSOLVED_ROW: str = "169837254" \
                    "53   28  " \
                    "8        " \
                    " 156    9" \
                    "6983   12" \
                    "3    9586" \
                    "  3     8" \
                    "9864 3 25" \
                    "7512    3"

UNSOLVED_COL: str = "4 8   713" \
                    " 37 48295" \
                    " 253  468" \
                    " 7 2    6" \
                    "      3 9" \
                    "8    4  7" \
                    "58 4 967 " \
                    "74 85693 " \
                    "  6     4"


class TestPointingTuple(unittest.TestCase):
    def test_solver_clears_pencil_marks_in_row(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_ROW)
        solver: Solver = Solver(sudoku)
        keys_to_change = ((3, 5), (4, 5))
        pointing_tuple = ((1, 5), (2, 5))
        digit = 7

        edited = {
            (7, 1): {7},
            (6, 2): {1, 7},
            (7, 2): {7},
            (6, 6): {4},
            (7, 6): {4}
        }
        sudoku.post_init(edited)

        self.assertTrue(solver.check_for_pointing_tuple())

        for key in keys_to_change:
            self.assertFalse(digit in sudoku[key].pencil_marks)
        for key in pointing_tuple:
            self.assertTrue(digit in sudoku[key].pencil_marks)

    def test_solver_clears_pencil_marks_in_col(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_COL)
        solver: Solver = Solver(sudoku)
        keys_to_change = ((0, 3), (0, 4), (0, 8))
        pointing_tuple = ((0, 1), (0, 2))

        self.assertTrue(solver.check_for_pointing_tuple())

        for key in keys_to_change:
            self.assertFalse(1 in sudoku[key].pencil_marks)
        for key in pointing_tuple:
            self.assertTrue(1 in sudoku[key].pencil_marks)


if __name__ == '__main__':
    unittest.main()
