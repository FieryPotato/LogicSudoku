import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

EASY_UNSOLVED = "6    85  " \
                "  8 97  3" \
                "  4 3  6 " \
                " 7  43   " \
                " 539 274 " \
                "   7   2 " \
                " 1  8    " \
                "8  17 2  " \
                "  2   1 7"

EASY_SOLVED = "631428579" \
              "528697413" \
              "794531862" \
              "276843951" \
              "153962748" \
              "489715326" \
              "317284695" \
              "865179234" \
              "942356187"


class TestFullSolve(unittest.TestCase):
    def test_easy_solve(self):
        unsolved = Sudoku.from_string(EASY_UNSOLVED)
        solved = Sudoku.from_string(EASY_SOLVED)
        solver = Solver(unsolved)
        solver.main()
        self.assertTrue(solver.is_solved)
        self.assertEqual(solved, solver.sudoku)


if __name__ == '__main__':
    unittest.main()
