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

COL_PAIR: str = " 24  31  " \
                " 7   26  " \
                "13   4   " \
                "     9725" \
                "   721   " \
                "7 25 6 1 " \
                "     7 89" \
                "  96 5 71" \
                "  7  83  "

COL_TRIPLE: str = "   2571  " \
                  "5 741 3  " \
                  "2 138   5" \
                  "   1 4 3 " \
                  "   9 8   " \
                  " 9 6 5   " \
                  "673891254" \
                  "   742863" \
                  "  2563   "

COL_QUADRUPLE: str = " 5  9    " \
                     " 1654    " \
                     " 49 7 516" \
                     "     7 5 " \
                     "  5   82 " \
                     " 3145  6 " \
                     "59    27 " \
                     "     56  " \
                     "   73   5"

BOX_PAIR: str = " 91      " \
                " 3 8 9 2 " \
                " 2  5  9 " \
                "6 3 98 7 " \
                "   2 7   " \
                " 8  6 4  " \
                " 6 38  4 " \
                "31   6 8 " \
                " 7    653"

BOX_TRIPLE: str = " 31   2  " \
                  "    23   " \
                  " 268  347" \
                  " 9   2 8 " \
                  "  5 7 4  " \
                  " 1 9   6 " \
                  "35   46  " \
                  "1  2     " \
                  "  9   17 "


class TestNakedRowTuples(unittest.TestCase):
    def test_solver_clears_naked_pairs_in_row(self):
        sudoku: Sudoku = Sudoku.from_string(ROW_PAIR)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((1, 8), (6, 8), (8, 8))
        naked_pair: tuple = ((4, 8), (5, 8))
        pair_options = {3, 9}

        self.assertTrue(solver.check_for_naked_tuples())

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertFalse(digit in pair_options)
        for key in naked_pair:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in pair_options)

    def test_solver_clears_naked_triples_in_row(self):
        sudoku: Sudoku = Sudoku.from_string(ROW_TRIPLE)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((0, 7), (1, 7), (2, 7))
        naked_triple: tuple = ((6, 7), (7, 7), (8, 7))
        triple_options: set = {3, 4, 6}

        # Two preliminary calls to clear the way for testing on the triple
        solver.check_for_naked_tuples()
        solver.check_for_naked_tuples()

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


class TestNakedColumnTuples(unittest.TestCase):
    def test_solver_clears_naked_pairs_in_column(self):
        sudoku: Sudoku = Sudoku.from_string(COL_PAIR)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((7, 4), (7, 8))
        naked_pair: tuple = ((7, 0), (7, 2))
        pair_options = {5, 9}

        solver.check_for_naked_tuples()
        self.assertTrue(solver.check_for_naked_tuples())

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertFalse(digit in pair_options)
        for key in naked_pair:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in pair_options)

    def test_solver_clears_naked_triples_in_column(self):
        sudoku: Sudoku = Sudoku.from_string(COL_TRIPLE)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((1, 0), (1, 3), (1, 4), (1, 7))
        naked_triple: tuple = ((1, 1), (1, 2), (1, 8))
        triple_options = {4, 6, 8}

        # eliminate naked triple in row 9
        solver.check_for_naked_tuples()
        self.assertTrue(solver.check_for_naked_tuples())

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertFalse(digit in triple_options)
        for key in naked_triple:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in triple_options)

    def test_solver_clears_naked_quadruples_in_column(self):
        sudoku: Sudoku = Sudoku.from_string(COL_QUADRUPLE)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((0, 3), (0, 4), (0, 7), (0, 8))
        naked_triple: tuple = ((0, 0), (0, 1), (0, 2), (0, 5))
        quadruple_options = {2, 3, 7, 8}

        solver.check_for_naked_tuples()
        solver.check_for_naked_tuples()
        self.assertTrue(solver.check_for_naked_tuples())

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertFalse(digit in quadruple_options)
        for key in naked_triple:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in quadruple_options)

    def test_solver_clears_naked_pairs_in_box(self):
        sudoku: Sudoku = Sudoku.from_string(BOX_PAIR)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((0, 4), (0, 5), (2, 4), (2, 5))
        naked_pair: tuple = ((1, 3), (1, 4))
        pair_options = {4, 5}

        self.assertTrue(solver.check_for_naked_pairs())

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertFalse(digit in pair_options)
        for key in naked_pair:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in pair_options)

    def test_solver_clears_naked_triples_in_box(self):
        sudoku: Sudoku = Sudoku.from_string(BOX_TRIPLE)
        solver: Solver = Solver(sudoku)
        keys_to_change: tuple = ((7, 7), (8, 7), (8, 8))
        naked_triple: tuple = ((7, 6), (8, 6), (6, 7))
        triple_options = {2, 8, 9}

        solver.check_for_naked_tuples()
        solver.check_for_naked_tuples()
        self.assertTrue(solver.check_for_naked_tuples())

        for key in keys_to_change:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertFalse(digit in triple_options)
        for key in naked_triple:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in triple_options)



if __name__ == '__main__':
    unittest.main()
