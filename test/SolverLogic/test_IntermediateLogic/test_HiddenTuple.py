"""
If two, three, or four digits can only be placed in that many cells in
a row, column or box (i.e. two digits across two cells, three across
three, etc.) then pencil marks for any other digits can be eliminated
from those cells.
"""


import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

ROW_PAIR = " 19 3    " \
           "4 582  7 " \
           "         " \
           "69  857 4" \
           "57  4  8 " \
           "3487    2" \
           "95  7    " \
           " 8  194  " \
           "1   5 69 "

COL_PAIR = "  5    17" \
           "  9 5 8 4" \
           "71  4   5" \
           " 5 61 4  " \
           "       5 " \
           "  257419 " \
           "   42356 " \
           "5 4   3  " \
           "  3  5 4 " \

BOX_PAIR = " 5    9  " \
           "     54  " \
           "38 7   15" \
           "  85 2   " \
           "  79 48  " \
           "  38     " \
           " 354 8 6 " \
           "8 215   4" \
           "      589"

ROW_TRIPLE = "  2 1 8 6" \
             " 69 83 17" \
             "781 6    " \
             "846329175" \
             "973154  8" \
             "125876943" \
             " 97 31 84" \
             "6 45987  " \
             "  8 4    "

COL_TRIPLE = "2453 61 7" \
             "7834   6 " \
             "1967  3  " \
             "43   7   " \
             "82  3    " \
             "65 9   23" \
             "  8  34 6" \
             "  4    3 " \
             "3621   75"

BOX_TRIPLE = " 8 654 7 " \
             "463792185" \
             "527183496" \
             "  29 1   " \
             " 9 3   2 " \
             "   82 619" \
             "   2 8  1" \
             "2  41 9 8" \
             " 1 539 6 "

ROW_QUADRUPLE = " 6 15 7  " \
                " 897 45  " \
                "57 86   3" \
                "4    68  " \
                "         " \
                " 973  4 5" \
                "9 8   651" \
                "   6 8927" \
                "7 6  53  "

COL_QUADRUPLE = " 148  2  " \
                " 98      " \
                "2753 6 81" \
                "86   5 3 " \
                "      5 8" \
                " 5 2  614" \
                "5 61   7 " \
                "   7  165" \
                "1 7  38  "

BOX_QUADRUPLE = "   34    " \
                "   5 6 2 " \
                "      9 7" \
                " 594  2  " \
                "2       6" \
                "8  1 275 " \
                "9 6      " \
                "18 6     " \
                "   983  2"


class TestHiddenTupleRow(unittest.TestCase):
    def test_solver_clears_pairs(self):
        sudoku = Sudoku.from_string(ROW_PAIR)
        solver = Solver(sudoku)
        pair = ((2, 6), (3, 6))
        options = {4, 6}

        edited = {
            (3, 0): {4},
            (5, 0): {6},
            (2, 2): {2},
            (3, 2): {4},
            (5, 2): {1, 6},
            (5, 4): {1, 6},
            (2, 6): {2},
            (5, 6): {4, 6},
            (2, 7): {2},
            (2, 8): {2},
            (5, 8): {4}
        }
        sudoku.post_init(edited)

        self.assertTrue(solver.check_for_hidden_tuple())

        for key in pair:
            self.assertEqual(options, sudoku[key].pencil_marks)

    def test_solver_clears_triples(self):
        sudoku = Sudoku.from_string(ROW_TRIPLE)
        solver = Solver(sudoku)
        triple = ((1, 8), (7, 8), (8, 8))
        options = {1, 5, 9}
        cells_to_clear = {(0, 8), (6, 8)}

        for key in cells_to_clear:
            for digit in options:
                if digit in (cell := sudoku[key].pencil_marks):
                    cell.remove(digit)

        self.assertTrue(solver.check_for_hidden_tuple())

        for key in triple:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in options)

    def test_solver_clears_quadruples(self):
        sudoku = Sudoku.from_string(ROW_QUADRUPLE)
        solver = Solver(sudoku)
        quadruple = ((0, 4), (3, 4), (4, 4), (8, 4))
        options = {4, 6, 8, 9}

        self.assertTrue(solver.check_for_hidden_tuple())

        for key in quadruple:
            for digit in options:
                if digit in (cell := sudoku[key].pencil_marks):
                    cell.remove(digit)


class TestHiddenTupleColumn(unittest.TestCase):
    def test_solver_clears_pairs(self):
        sudoku = Sudoku.from_string(COL_PAIR)
        solver = Solver(sudoku)
        changed = ((5, 1), (5, 7))
        options = {1, 7}
        edited = {
            (6, 0): {2},
            (3, 1): {2, 3},
            (5, 1): {2, 6},
            (6, 2): {2},
            (0, 3): {8},
            (5, 3): {8},
            (7, 3): {2, 3},
            (8, 3): {8},
            (6, 4): {6},
            (7, 7): {2},
            (6, 8): {9}
        }
        sudoku.post_init(edited)

        self.assertTrue(solver.check_for_hidden_tuple())

        for key in changed:
            self.assertEqual(options, sudoku[key].pencil_marks)

    def test_solver_clears_triples(self):
        sudoku = Sudoku.from_string(COL_TRIPLE)
        solver = Solver(sudoku)
        triple = ((4, 3), (4, 6), (4, 7))
        options = {2, 6, 7}
        cells_to_clear = {(4, 1), (4, 2)}

        for key in cells_to_clear:
            for digit in options:
                if digit in (cell := sudoku[key].pencil_marks):
                    cell.remove(digit)

        self.assertTrue(solver.check_for_hidden_tuple())

        for key in triple:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in options)

    def test_solver_clears_quadruples(self):
        sudoku = Sudoku.from_string(COL_QUADRUPLE)
        solver = Solver(sudoku)
        quadruple = ((4, 0), (4, 4), (4, 5), (4, 8))
        options = {3, 5, 6, 7}

        self.assertTrue(solver.check_for_hidden_tuple())

        for key in quadruple:
            for digit in options:
                if digit in (cell := sudoku[key].pencil_marks):
                    cell.remove(digit)


class TestHiddenTupleBox(unittest.TestCase):
    def test_solver_clears_pairs(self):
        sudoku = Sudoku.from_string(BOX_PAIR)
        solver = Solver(sudoku)
        pair = ((7, 3), (7, 5))
        options = {4, 9}

        edited = {
            (5, 0): {6},
            (5, 5): {6},
            (0, 6): {1},
            (4, 6): {2},
            (6, 6): {7},
            (8, 6): {7},
            (1, 7): {7},
            (5, 7): {3, 7},
            (5, 8): {6}
        }
        sudoku.post_init(edited)

        self.assertTrue(solver.check_for_hidden_tuple())

        for key in pair:
            self.assertEqual(options, sudoku[key].pencil_marks)

    def test_solver_clears_triples(self):
        sudoku = Sudoku.from_string(BOX_TRIPLE)
        solver = Solver(sudoku)
        triple = ((0, 3), (0, 4), (1, 4))
        options = {1, 6, 8}

        self.assertTrue(solver.check_for_hidden_tuple())

        for key in triple:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in options)

    def test_solver_clears_quadruples(self):
        sudoku = Sudoku.from_string(BOX_QUADRUPLE)
        solver = Solver(sudoku)
        quadruple = ((1, 0), (2, 0), (1, 1), (2, 1))
        options = {1, 2, 8, 9}

        edited = {
            (0, 0): {5},
            (2, 0): {5},
            (5, 0): {1, 8},
            (4, 1): {1},
            (1, 2): {1, 2},
            (2, 2): {1, 2, 8},
            (7, 2): {1, 8},
            (4, 3): {7, 8},
            (5, 3): {1, 2, 3, 4, 5, 6, 9},
            (3, 4): {1, 2, 3, 4, 5, 6, 9},
            (4, 4): {7, 8},
            (5, 4): {7, 8},
            (6, 4): {1},
            (7, 4): {1},
            (4, 5): {7, 8},
            (8, 5): {1},
            (1, 6): {4, 7},
            (6, 6): {1},
            (7, 6): {1},
            (8, 6): {1},
            (2, 7): {4, 5, 7},
            (6, 7): {1},
            (7, 7): {1},
            (8, 7): {1},
            (0, 8): {1},
            (1, 8): {1},
            (2, 8): {6},
            (6, 8): {2, 3, 4, 5, 7, 8, 9},
            (7, 8): {2, 3, 4, 5, 7, 8, 9}
        }
        sudoku.post_init(edited)

        self.assertTrue(solver.check_for_hidden_tuple())

        for key in quadruple:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in options)


if __name__ == '__main__':
    unittest.main()
