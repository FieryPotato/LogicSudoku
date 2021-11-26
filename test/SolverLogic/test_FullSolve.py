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

INTERMEDIATE_UNSOLVED = " 8    6 5" \
                        "2   5 7  " \
                        "76      9" \
                        " 1 9 3   " \
                        "  4   1  " \
                        "   5 1 8 " \
                        "6    2 14" \
                        "  8 6   7" \
                        "1 3      "

INTERMEDIATE_SOLVED = "381297645" \
                      "249658731" \
                      "765314829" \
                      "812943576" \
                      "534786192" \
                      "976521483" \
                      "657832914" \
                      "428169357" \
                      "193475268"

HARD_UNSOLVED = " 9  8   1" \
                "78       " \
                " 2 3  84 " \
                "  6    2 " \
                "    5    " \
                " 4 6  9  " \
                "  4  2 8 " \
                "        9" \
                "85  7  63"

HARD_SOLVED = "493287651" \
              "781546392" \
              "625391847" \
              "936718524" \
              "218459736" \
              "547623918" \
              "374962185" \
              "162835479" \
              "859174263"

BRUTAL_UNSOLVED = "   4     " \
                  "    9 31 " \
                  " 2  574 6" \
                  "      7 4" \
                  " 7  6  2 " \
                  "  9      " \
                  "7 481  6 " \
                  " 63  5   " \
                  " 5   2   "

BRUTAL_SOLVED = "536481279" \
                "847296315" \
                "921357486" \
                "612538794" \
                "475169823" \
                "389724651" \
                "794813562" \
                "263975148" \
                "158642937"


@unittest.skip("Full Solve tests take too long.")
class TestFullSolve(unittest.TestCase):
    def test_easy_solve(self):
        unsolved = Sudoku.from_string(EASY_UNSOLVED)
        solved = Sudoku.from_string(EASY_SOLVED)
        solver = Solver(unsolved)
        self.assertTrue(solver.main())
        self.assertEqual(solved, solver.sudoku)

    def test_intermediate_solve(self):
        unsolved = Sudoku.from_string(INTERMEDIATE_UNSOLVED)
        solved = Sudoku.from_string(INTERMEDIATE_SOLVED)
        solver = Solver(unsolved)
        self.assertTrue(solver.main())
        self.assertEqual(solved, solver.sudoku)

    def test_hard_solve(self):
        unsolved = Sudoku.from_string(HARD_UNSOLVED)
        solved = Sudoku.from_string(HARD_SOLVED)
        solver = Solver(unsolved)
        self.assertTrue(solver.main())
        self.assertEqual(solved, solver.sudoku)

    def test_brutal_solve(self):
        unsolved = Sudoku.from_string(BRUTAL_UNSOLVED)
        solved = Sudoku.from_string(BRUTAL_SOLVED)
        solver = Solver(unsolved)
        self.assertTrue(solver.main())
        self.assertEqual(solved, solver.sudoku)



if __name__ == '__main__':
    unittest.main()
