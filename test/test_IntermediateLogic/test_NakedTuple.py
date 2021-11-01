import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

ROW_PAIR: str = " 2   7  8" \
                "7  2  49 " \
                "    45721" \
                "     12  " \
                "9 7624  5" \
                "  2      " \
                "6 315287 " \
                " 7 486  2" \
                "2 87   6 "

ROW_TRIPLE: str = " 98235   " \
                  "   179   " \
                  "5  648 9 " \
                  " 6   4  9" \
                  "  7 61354" \
                  "4    2   " \
                  "     3  1" \
                  "   527   " \
                  "  341698 "

ROW_QUADRUPLE: str = "     6574" \
                     "7  5  26 " \
                     "    7    " \
                     "486752   " \
                     "5       7" \
                     "9 71  45 " \
                     "   82    " \
                     " 7 9143  " \
                     "  863    "


class TestNakedRowTuples(unittest.TestCase):
    def test_solver_clears_naked_pairs_in_row(self):
        sudoku: Sudoku = Sudoku.from_string(ROW_PAIR)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((1, 8), (6, 8), (8, 8))
        naked_pair: tuple = ((4, 8), (5, 8))

        self.assertTrue(solver.check_for_naked_tuples())

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            self.assertFalse(3 in pencil_marks or 9 in pencil_marks)
        for key in naked_pair:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in {3, 9})

    def test_solver_clears_naked_triples_in_row(self):
        sudoku: Sudoku = Sudoku.from_string(ROW_TRIPLE)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((0, 7), (1, 7), (2, 7))
        naked_triple: tuple = ((6, 7), (7, 7), (8, 7))
        triple_options: set = {3, 4, 6}

        solver.check_for_naked_tuples()  # first run to clear 8,9 pair on (3, 6) and (4, 6)
        self.assertTrue(solver.check_for_naked_tuples())

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertFalse(digit in triple_options)
        for key in naked_triple:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in triple_options)

    def test_solver_clears_naked_quadruples_in_row(self):
        sudoku: Sudoku = Sudoku.from_string(ROW_QUADRUPLE)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((0, 2), (1, 2), (2, 2), (3, 2))
        naked_quadruple: tuple = ((5, 2), (6, 2), (7, 2), (8, 2))
        quadruple_options: set = {1, 3, 8, 9}

        self.assertTrue(solver.check_for_naked_tuples())

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertFalse(digit in quadruple_options)
        for key in naked_quadruple:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in quadruple_options)


if __name__ == '__main__':
    unittest.main()
