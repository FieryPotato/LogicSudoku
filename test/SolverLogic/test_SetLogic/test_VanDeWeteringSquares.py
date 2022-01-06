import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku

minor_keys_0 = [(5, 8), (5, 7), (5, 6), (5, 5), (6, 5), (7, 5), (8, 5)]
major_keys_0 = [(3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3), (4, 0),
                (4, 1), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4), (1, 4), (0, 4)]
minor_keys_1 = [(0, 5), (1, 5), (2, 5), (3, 5), (3, 6), (3, 7), (3, 8)]
major_keys_1 = [(4, 0), (5, 0), (4, 1), (5, 1), (4, 2), (5, 2), (4, 3), (5, 3),
                (4, 4), (5, 4), (6, 3), (6, 4), (7, 3), (7, 4), (8, 3), (8, 4)]
minor_keys_2 = [(5, 0), (5, 1), (5, 2), (5, 3), (6, 3), (7, 3), (8, 3)]
major_keys_2 = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (4, 5), (4, 6), (4, 7),
                (4, 8), (0, 5), (1, 5), (2, 5), (3, 5), (3, 6), (3, 7), (3, 8)]
minor_keys_3 = [(3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3)]
major_keys_3 = [(4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (4, 5), (5, 5), (6, 5),
                (7, 5), (8, 5), (4, 6), (5, 6), (4, 7), (5, 7), (4, 8), (5, 8)]


class TestVanDeWeteringSquareInSudoku(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.sudoku = Sudoku()
        self.minor_cells_0 = {self.sudoku[key] for key in minor_keys_0}
        self.major_cells_0 = {self.sudoku[key] for key in major_keys_0}
        self.minor_cells_1 = {self.sudoku[key] for key in minor_keys_1}
        self.major_cells_1 = {self.sudoku[key] for key in major_keys_1}
        self.minor_cells_2 = {self.sudoku[key] for key in minor_keys_2}
        self.major_cells_2 = {self.sudoku[key] for key in major_keys_2}
        self.minor_cells_3 = {self.sudoku[key] for key in minor_keys_3}
        self.major_cells_3 = {self.sudoku[key] for key in major_keys_3}

    def test_sudoku_generates_single_vdw_square(self):
        tl = self.sudoku.single_vdw_square("top", "left")
        tr = self.sudoku.single_vdw_square("top", "right")
        bl = self.sudoku.single_vdw_square("bottom", "left")
        br = self.sudoku.single_vdw_square("bottom", "right")

        self.assertEqual(self.major_cells_0, tl[0])
        self.assertEqual(self.minor_cells_0, tl[1])
        self.assertEqual(self.major_cells_1, tr[0])
        self.assertEqual(self.minor_cells_1, tr[1])
        self.assertEqual(self.major_cells_2, bl[0])
        self.assertEqual(self.minor_cells_2, bl[1])
        self.assertEqual(self.major_cells_3, br[0])
        self.assertEqual(self.minor_cells_3, br[1])

    def test_sudoku_generates_all_vdw_squares(self):
        expected = [(self.major_cells_0, self.minor_cells_0), (self.major_cells_1, self.minor_cells_1),
                    (self.major_cells_2, self.minor_cells_2), (self.major_cells_3, self.minor_cells_3)]

        self.assertEqual(expected, self.sudoku.vdw_squares())



class TestVDWSingleDigitPlacement(unittest.TestCase):
    def test_solver_clears_single_vdw_major_digit(self):
        unsolved = "   85    " \
                   "   96    " \
                   "   41    " \
                   "9 437    " \
                   "62758    " \
                   "     4576" \
                   "     8   " \
                   "     9   " \
                   "     5   "

        sudoku = Sudoku.from_string(unsolved)
        solver = Solver(sudoku)

        cell = sudoku[1, 3]
        digit = 5

        self.assertTrue(solver.check_for_vdw_square_singles())
        self.assertEqual(cell.digit, digit)


    def test_solver_clears_single_vdw_minor_digit(self):
        unsolved = "     9   " \
                   "     5   " \
                   "     7   " \
                   "     61 4" \
                   "24357    " \
                   "16749    " \
                   "   71    " \
                   "   95    " \
                   "   68    "
        sudoku = Sudoku.from_string(unsolved)
        solver = Solver(sudoku)

        cell = sudoku[7, 3]
        digit = 7

        self.assertTrue(solver.check_for_vdw_square_singles())


if __name__ == '__main__':
    unittest.main()
