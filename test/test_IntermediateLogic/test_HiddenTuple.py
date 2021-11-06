import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

ROW_PAIR = "      456" \
           "5 734   2" \
           " 942 5 8 " \
           "4 95     " \
           "  16 254 " \
           "  54 7   " \
           "95 1   34" \
           "     42  " \
           " 4    6  "

COL_PAIR = "   8697  " \
           " 7 34568 " \
           "6 8271 3 " \
           "   483  5" \
           "    57  8" \
           "8  6 2 4 " \
           " 235 84 6" \
           "184726   " \
           "  6 348  "

BOX_PAIR = "6  1  27 " \
           "   9  6  " \
           "3  276  4" \
           "  6 3  25" \
           "  9 683  " \
           "73  2  6 " \
           "5  61  32" \
           " 638 2   " \
           " 1 3    6"

ROW_TRIPLE = "  2 1 8 6" \
             " 69 83 17" \
             "781 6    " \
             "846329175" \
             "973154  8" \
             "125876943" \
             " 97 31 84" \
             "6 45987  " \
             "  8 4    "


class TestHiddenTupleRow(unittest.TestCase):
    def test_solver_clears_pairs(self):
        sudoku = Sudoku.from_string(ROW_PAIR)
        solver = Solver(sudoku)
        pair = ((1, 3), (7, 3))
        options = {2, 6}

        solver.check_for_hidden_tuples()
        self.assertTrue(solver.check_for_hidden_tuples())

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

        self.assertTrue(solver.check_for_hidden_tuples())

        for key in triple:
            pencil_marks = sudoku[key].pencil_marks
            for digit in pencil_marks:
                self.assertTrue(digit in options)


class TestHiddenTupleColumn(unittest.TestCase):
    def test_solver_clears_pairs(self):
        sudoku = Sudoku.from_string(COL_PAIR)
        solver = Solver(sudoku)
        pair = ((0, 0), (0, 4))
        options = {3, 4}

        self.assertTrue(solver.check_for_hidden_tuples())

        for key in pair:
            self.assertEqual(options, sudoku[key].pencil_marks)


class TestHiddenTupleBox(unittest.TestCase):
    def test_solver_clears_pairs(self):
        sudoku = Sudoku.from_string(BOX_PAIR)
        solver = Solver(sudoku)
        pair = ((5, 3), (5, 5))
        options = {1, 9}

        self.assertTrue(solver.check_for_hidden_tuples())

        for key in pair:
            self.assertEqual(options, sudoku[key].pencil_marks)


if __name__ == '__main__':
    unittest.main()
