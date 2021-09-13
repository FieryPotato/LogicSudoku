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

UNSOLVED_COL: str = ""


class TestPointingTuple(unittest.TestCase):
    def test_solver_clears_pencil_marks_in_row(self) -> None:
        sudoku: Sudoku = Sudoku().from_string(UNSOLVED_ROW)
        solver: Solver = Solver(sudoku)
        keys_to_change = ((3, 5), (4, 5))
        pointing_tuple = ((1, 5), (2, 5))

        solver.check_for_pointing_tuple()

        for key in keys_to_change:
            self.assertFalse(7 in sudoku[key].pencil_marks)
        for key in pointing_tuple:
            self.assertTrue(7 in sudoku[key].pencil_marks)


if __name__ == '__main__':
    unittest.main()
