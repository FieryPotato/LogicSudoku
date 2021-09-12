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


class TestLockedCandidate(unittest.TestCase):
    def test_solver_clears_pencil_marks_for_locked_candidates_in_row(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_ROW)
        solver: Solver = Solver(sudoku)
        keys_to_change = ((0, 6), (1, 6), (2, 6), (0, 7))
        locked_candidates = ((1, 8), (2, 8))

        solver.check_for_locked_candidates()

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            self.assertFalse(3 in pencil_marks)
        for key in locked_candidates:
            pencil_marks = sudoku[key].pencil_marks
            self.assertTrue(3 in pencil_marks)


if __name__ == '__main__':
    unittest.main()
