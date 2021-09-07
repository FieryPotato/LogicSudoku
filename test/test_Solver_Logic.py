import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


class testNakedSingle(unittest.TestCase):
    unsolved: str = "8 4915627915726834672348519186497253347652981529183476498231765261579348753864192"

    def test_solver_fills_naked_singles(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(self.unsolved)
        solver: Solver = Solver(sudoku)
        solver.fill_naked_singles()
        self.assertEqual(3, solver.sudoku[(1, 0)].digit)


class testHiddenSingle(unittest.TestCase):
    unsolved_row: str = "    9   5  3  2 4 5     2  7 8    92 1  7  8  5      3  5       6 7  3  19  64   "
    unsolved_col: str = "6  89541  5 621   1  743   9  582    4 179 5    364  8  3 56  1     8 7   94 7  2"
    unsolved_box: str = "12 9 7  4 4 2        43    63 5 1   4 587 6     3   9 8  7 5      6   7 9      48"

    def test_solver_fills_hidden_singles_in_row(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(self.unsolved_row)
        solver: Solver = Solver(sudoku)
        solver.fill_hidden_singles()
        self.assertEqual(3, solver.sudoku[(3, 8)].digit)

    def test_solver_fills_hidden_singles_in_col(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(self.unsolved_col)
        solver: Solver = Solver(sudoku)
        solver.fill_hidden_singles()
        self.assertEqual(9, solver.sudoku[(1, 2)].digit)

    def test_solver_fills_hidden_singles_in_box(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(self.unsolved_box)
        solver: Solver = Solver(sudoku)
        solver.fill_hidden_singles()
        self.assertEqual(1, solver.sudoku[(4, 1)].digit)


if __name__ == "__main__":
    unittest.main()
