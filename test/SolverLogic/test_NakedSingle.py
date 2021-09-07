import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

UNSOLVED: str = "8 4915627" \
                "915726834" \
                "672348519" \
                "186497253" \
                "347652981" \
                "529183476" \
                "498231765" \
                "261579348" \
                "753864192"


class TestNakedSingle(unittest.TestCase):
    """A naked single is a cell which only contains one valid option."""

    def test_solver_fills_naked_singles(self) -> None:
        sudoku: Sudoku = Sudoku.from_string(UNSOLVED)
        solver: Solver = Solver(sudoku)
        solver.fill_naked_singles()
        self.assertEqual(3, solver.sudoku[(1, 0)].digit)


if __name__ == '__main__':
    unittest.main()
