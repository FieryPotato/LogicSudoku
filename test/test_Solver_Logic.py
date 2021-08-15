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
    unsolved_row: str = "  8923714742168 3993147 62839 68427181423796 267 198431863924 7 297413864738 6192"
    unsolved_col: str = " 58923 14 421685399314 56283956842 181423 96526 51984318639245 529 413864 3856192"

    def test_solver_fills_hidden_singles_in_row(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(self.unsolved_row)
        solver: Solver = Solver(sudoku)
        solver.fill_hidden_singles()
        self.assertEqual(5, solver.sudoku[(1, 0)].digit)


if __name__ == "__main__":
    unittest.main()
