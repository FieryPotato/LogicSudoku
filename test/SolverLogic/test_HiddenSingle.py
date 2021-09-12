import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

UNSOLVED_ROW: str = "    9   5" \
                    "  3  2 4 " \
                    "5     2  " \
                    "7 8    92" \
                    " 1  7  8 " \
                    " 5      3" \
                    "  5      " \
                    " 6 7  3  " \
                    "19  64   "

UNSOLVED_COL: str = "6  89541 " \
                    " 5 621   " \
                    "1  743   " \
                    "9  582   " \
                    " 4 179 5 " \
                    "   364  8" \
                    "  3 56  1" \
                    "     8 7 " \
                    "  94 7  2"

UNSOLVED_BOX: str = "12 9 7  4" \
                    " 4 2     " \
                    "   43    " \
                    "63 5 1   " \
                    "4 587 6  " \
                    "   3   9 " \
                    "8  7 5   " \
                    "   6   7 " \
                    "9      48"


class TestHiddenSingle(unittest.TestCase):
    """A hidden single is a cell which contains a unique option in its
    row, column, or box."""

    def test_solver_fills_hidden_singles_in_row(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_ROW)
        solver: Solver = Solver(sudoku)
        solver.fill_hidden_singles()
        self.assertEqual(3, solver.sudoku[(3, 8)].digit)

    def test_solver_fills_hidden_singles_in_col(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_COL)
        solver: Solver = Solver(sudoku)
        solver.fill_hidden_singles()
        self.assertEqual(9, solver.sudoku[(1, 2)].digit)

    def test_solver_fills_hidden_singles_in_box(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED_BOX)
        solver: Solver = Solver(sudoku)
        solver.fill_hidden_singles()
        self.assertEqual(1, solver.sudoku[(4, 1)].digit)

if __name__ == '__main__':
    unittest.main()
