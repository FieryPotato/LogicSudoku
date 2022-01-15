import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


class TestSolverStep(unittest.TestCase):
    def test_solver_step_only_does_one_thing(self):
        sudoku = Sudoku.from_string(
            "    3527 "
            " 4 67  3 "
            "738   5  "
            "     2 84"
            "8 37946 5"
            " 9       "
            " 5 8   9 "
            " 8  467 1"
            "91 2  8  "
        )
        solver = Solver(sudoku)
        self.assertTrue(solver.step())
        self.assertFalse(sudoku[1, 0].is_empty)
        self.assertTrue(sudoku[0, 0].is_empty)
        self.assertTrue(solver.step())
        self.assertFalse(sudoku[0, 0].is_empty)


# @unittest.skip("Run only separately")
class TestFullSolve(unittest.TestCase):
    easy_unsolved = "6    85  " \
                    "  8 97  3" \
                    "  4 3  6 " \
                    " 7  43   " \
                    " 539 274 " \
                    "   7   2 " \
                    " 1  8    " \
                    "8  17 2  " \
                    "  2   1 7"
    easy_solved = "631428579" \
                  "528697413" \
                  "794531862" \
                  "276843951" \
                  "153962748" \
                  "489715326" \
                  "317284695" \
                  "865179234" \
                  "942356187"
    intermediate_unsolved = " 8    6 5" \
                            "2   5 7  " \
                            "76      9" \
                            " 1 9 3   " \
                            "  4   1  " \
                            "   5 1 8 " \
                            "6    2 14" \
                            "  8 6   7" \
                            "1 3      "
    intermediate_solved = "381297645" \
                          "249658731" \
                          "765314829" \
                          "812943576" \
                          "534786192" \
                          "976521483" \
                          "657832914" \
                          "428169357" \
                          "193475268"
    hard_unsolved = " 9  8   1" \
                    "78       " \
                    " 2 3  84 " \
                    "  6    2 " \
                    "    5    " \
                    " 4 6  9  " \
                    "  4  2 8 " \
                    "        9" \
                    "85  7  63"
    hard_solved = "493287651" \
                  "781546392" \
                  "625391847" \
                  "936718524" \
                  "218459736" \
                  "547623918" \
                  "374962185" \
                  "162835479" \
                  "859174263"
    brutal_unsolved = "   4     " \
                      "    9 31 " \
                      " 2  574 6" \
                      "      7 4" \
                      " 7  6  2 " \
                      "  9      " \
                      "7 481  6 " \
                      " 63  5   " \
                      " 5   2   "
    brutal_solved = "536481279" \
                    "847296315" \
                    "921357486" \
                    "612538794" \
                    "475169823" \
                    "389724651" \
                    "794813562" \
                    "263975148" \
                    "158642937"
    galaxy_unsolved = "  98    3" \
                      "    9146 " \
                      "1     7  " \
                      "34   2 7 " \
                      "         " \
                      " 2 3 6 48" \
                      "     3  1" \
                      " 3 41    " \
                      "2    93  "
    galaxy_solved = "469827513" \
                    "783591462" \
                    "152634789" \
                    "346982175" \
                    "897145236" \
                    "521376948" \
                    "674253891" \
                    "935418627" \
                    "218769354"

    def test_easy(self):
        actual = Sudoku.from_string(self.easy_unsolved)
        expected = Sudoku.from_string(self.easy_solved)
        s = Solver(actual)
        self.assertTrue(s.main())
        self.assertTrue(expected, actual)

    def test_intermediate(self):
        actual = Sudoku.from_string(self.intermediate_unsolved)
        expected = Sudoku.from_string(self.intermediate_solved)
        s = Solver(actual)
        self.assertTrue(s.main())
        self.assertTrue(expected, actual)

    def test_hard(self):
        actual = Sudoku.from_string(self.hard_unsolved)
        expected = Sudoku.from_string(self.hard_solved)
        s = Solver(actual)
        self.assertTrue(s.main())
        self.assertTrue(expected, actual)

    def test_brutal(self):
        actual = Sudoku.from_string(self.brutal_unsolved)
        expected = Sudoku.from_string(self.brutal_solved)
        s = Solver(actual)
        self.assertTrue(s.main())
        self.assertTrue(expected, actual)

    def test_galaxy(self):
        actual = Sudoku.from_string(self.galaxy_unsolved)
        expected = Sudoku.from_string(self.galaxy_solved)
        s = Solver(actual)
        self.assertTrue(s.main())
        self.assertTrue(expected, actual)

if __name__ == '__main__':
    unittest.main()
