"""
Phistomephel's Theorem states that the set containing all cells in each
2x2 corner of a sudoku grid is identical to the set containing all
cells that line the outside of the center box. This sort of set
relation exists for many other similar organizations of rows and
columns.
"""

import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


class Test_Phistomephel_Prerequisites(unittest.TestCase):
    def setUp(self):
        self.sudoku = Sudoku()

    def test_sudoku_generates_base_phistomephel_set(self):
        corner_keys = {
            (0, 0), (1, 0), (0, 1), (1, 1), (7, 0), (8, 0), (7, 1), (8, 1),
            (0, 7), (1, 7), (0, 8), (1, 8), (7, 7), (8, 7), (7, 8), (8, 8)
        }
        ring_keys = {
            (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (2, 3), (6, 3), (2, 4),
            (6, 4), (2, 5), (6, 5), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6)
        }
        corner_cells = {self.sudoku[key] for key in corner_keys}
        ring_cells = {self.sudoku[key] for key in ring_keys}
        multi_set = self.sudoku.phistomephel_sets(2, 6, 2, 6)
        single_set = self.sudoku.single_phistomephel_set(2, 6, 2, 6)
        for result in multi_set, single_set:
            self.assertEqual(corner_cells, result[0])
            self.assertEqual(ring_cells, result[1])

    def test_sudoku_gets_all_phistomephel_sets(self):
        first_corner_keys = {
            (1, 1), (2, 1), (1, 2), (2, 2), (7, 1), (8, 1), (7, 2), (8, 2),
            (1, 7), (2, 7), (1, 8), (2, 8), (7, 7), (8, 7), (7, 8), (8, 8)
        }
        first_ring_keys = {
            (0, 0), (3, 0), (4, 0), (5, 0), (6, 0), (0, 3), (6, 3), (0, 4),
            (6, 4), (0, 5), (6, 5), (0, 6), (3, 6), (4, 6), (5, 6), (6, 6)
        }
        first_corner_cells = {self.sudoku[key] for key in first_corner_keys}
        first_ring_cells = {self.sudoku[key] for key in first_ring_keys}

        last_corner_keys = {
            (0, 0), (1, 0), (0, 1), (1, 1), (6, 0), (7, 0), (6, 1), (7, 1),
            (0, 6), (1, 6), (0, 7), (1, 7), (6, 6), (7, 6), (6, 7), (7, 7)
        }
        last_ring_keys = {
            (2, 2), (3, 2), (4, 2), (5, 2), (8, 2), (2, 3), (8, 3), (2, 4),
            (8, 4), (2, 5), (8, 5), (2, 8), (3, 8), (4, 8), (5, 8), (8, 8)
        }
        last_corner_cells = {self.sudoku[key] for key in last_corner_keys}
        last_ring_cells = {self.sudoku[key] for key in last_ring_keys}

        result = self.sudoku.phistomephel_sets()
        self.assertEqual(first_corner_cells, result[0][0])
        self.assertEqual(first_ring_cells, result[0][1])
        self.assertEqual(last_corner_cells, result[-1][0])
        self.assertEqual(last_ring_cells, result[-1][1])


class TestPhistomephelSingleDigitPlacement(unittest.TestCase):
    def setUp(self):
        self.missing_ring = "64     32" \
                            "35     79" \
                            "  83295  " \
                            "  1   2  " \
                            "  4   9  " \
                            "  5   3  " \
                            "  35 64  " \
                            "51     23" \
                            "48     95"

        self.missing_corner = "3 5   8 7" \
                              " 7 254 3 " \
                              "9 4     2" \
                              " 3     7 " \
                              " 4     2 " \
                              " 8     6 " \
                              "2 3   7 5" \
                              " 6 529 8 " \
                              "4 8   2 6"

    def test_solver_fills_missing_ring_digit(self):
        sudoku = Sudoku.from_string(self.missing_ring)
        solver = Solver(sudoku)
        missing_cell = sudoku[4, 6]
        digit = 7
        self.assertTrue(solver.check_for_phistomephel_singles())
        self.assertEqual(digit, missing_cell.digit)

    def test_solver_fills_missing_corner_digit(self):
        sudoku = Sudoku.from_string(self.missing_corner)
        solver = Solver(sudoku)
        missing_cell = sudoku[6, 2]
        digit = 6
        self.assertTrue(solver.check_for_phistomephel_singles())
        self.assertEqual(digit, missing_cell.digit)



if __name__ == '__main__':
    unittest.main()
