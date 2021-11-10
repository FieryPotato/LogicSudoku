"""
If the only places for a digit in a row or column share a box, the other
cells in that box cannot contain that digit.
"""


import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

UNSOLVED_ROW: str = "75  21  4" \
                    "  9  3 8 " \
                    "  6      " \
                    " 72  6849" \
                    "864 9 3  " \
                    "9   84 6 " \
                    "    6 41 " \
                    " 415 8   " \
                    "6  41  58"

UNSOLVED_COL: str = " 5 9     " \
                    " 1   8   " \
                    "3 2 6   8" \
                    "9 4  6   " \
                    "7 6   9 5" \
                    " 2  398 6" \
                    " 6    5 7" \
                    "   6  28 " \
                    "    45 6 "


class TestLockedCandidate(unittest.TestCase):
    def test_solver_clears_pencil_marks_in_row(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_ROW)
        solver: Solver = Solver(sudoku)
        keys_to_change = ((0, 6), (1, 6), (2, 6), (0, 7))
        locked_candidates = ((1, 8), (2, 8))

        self.assertTrue(solver.check_for_locked_candidates())

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            self.assertFalse(3 in pencil_marks)
        for key in locked_candidates:
            pencil_marks = sudoku[key].pencil_marks
            self.assertTrue(3 in pencil_marks)

    def test_solver_clears_pencil_marks_in_column(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_COL)
        solver: Solver = Solver(sudoku)
        keys_to_change = ((7, 0), (8, 0), (7, 1), (8, 1), (7, 2))
        locked_candidates = ((6, 0), (6, 1), (6, 2))

        self.assertTrue(solver.check_for_locked_candidates())

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            self.assertFalse(4 in pencil_marks)
        for key in locked_candidates:
            pencil_marks = sudoku[key].pencil_marks
            self.assertTrue(4 in pencil_marks)


if __name__ == '__main__':
    unittest.main()
