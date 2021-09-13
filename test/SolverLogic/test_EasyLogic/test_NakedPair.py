import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


UNSOLVED_ROW: str = " 2   7  8" \
                    "7  2  49 " \
                    "    45721" \
                    "     12  " \
                    "9 7624  5" \
                    "  2      " \
                    "6 315287 " \
                    " 7 486  2" \
                    "2 87   6 "

UNSOLVED_BOX: str = " 91      " \
                    " 3 8 9 2 " \
                    " 2  5  9 " \
                    "6 3 98 7 " \
                    "   2 7   " \
                    " 8  6 4  " \
                    " 6 38  4 " \
                    "31   6 8 " \
                    " 7    653"

UNSOLVED_COL: str = " 24  31  " \
                    " 7   26  " \
                    "13   4   " \
                    "     9725" \
                    "   721   " \
                    "7 25 6 1 " \
                    "     7 89" \
                    "  96 5 71" \
                    "  7  83  "


class TestNakedPair(unittest.TestCase):
    def test_solver_clears_pencil_marks_for_naked_pairs_in_box(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_BOX)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((0, 4), (0, 5), (2, 4), (2, 5))
        naked_pair: tuple = ((1, 3), (1, 4))

        solver.check_for_naked_pairs()

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            self.assertFalse(4 in pencil_marks or 5 in pencil_marks)
        for key in naked_pair:
            pencil_marks = sudoku[key].pencil_marks
            self.assertTrue(4 in pencil_marks and 5 in pencil_marks and len(pencil_marks) == 2)

    def test_solver_clears_pencil_marks_for_naked_pairs_in_row(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_ROW)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((1, 8), (6, 8), (8, 8))
        naked_pair: tuple = ((4, 8), (5, 8))

        solver.check_for_naked_pairs()

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            self.assertFalse(3 in pencil_marks or 9 in pencil_marks)
        for key in naked_pair:
            pencil_marks = sudoku[key].pencil_marks
            self.assertTrue(3 in pencil_marks and 9 in pencil_marks and len(pencil_marks) == 2)

    def test_solver_clears_pencil_marks_for_naked_pairs_in_col(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_COL)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((7, 4), (7, 8))
        naked_pair: tuple = ((7, 0), (7, 2))

        solver.check_for_naked_pairs()

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            self.assertFalse(5 in pencil_marks or 9 in pencil_marks)
        for key in naked_pair:
            pencil_marks = sudoku[key].pencil_marks
            self.assertTrue(5 in pencil_marks and 9 in pencil_marks and len(pencil_marks) == 2)


if __name__ == '__main__':
    unittest.main()
