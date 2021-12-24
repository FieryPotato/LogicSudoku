import unittest

from src.Solver import Solver, find_empty_rectangle_house
from src.Sudoku import Sudoku


class TestEmptyRectangleFunctions(unittest.TestCase):
    def setUp(self) -> None:
        unsolved = "  857 6 4" \
                   "46   2 75" \
                   "5 74   3 " \
                   "94 1   8 " \
                   "   8 5   " \
                   " 8 2    1" \
                   " 5 6 4  7" \
                   "8 475  26" \
                   "176 2 45 "
        self.sudoku = Sudoku.from_string(unsolved)
        edited = {
            (1, 0): {9},
            (6, 1): {9},
            (1, 2): {2},
            (4, 2): {8},
            (6, 2): {8},
            (6, 3): {3},
            (0, 4): {2, 3},
            (4, 4): {6},
            (7, 4): {9},
            (0, 5): {3},
            (4, 5): {6},
            (5, 5): {6},
            (7, 5): {9},
            (4, 6): {9}
        }
        self.sudoku.post_init(edited)
        self.solver = Solver(self.sudoku)

    def test_house_contains_filled_digit(self):
        self.assertFalse(self.sudoku.house_contains_filled_digit("box", house_num=0, digit=1))
        self.assertTrue(self.sudoku.house_contains_filled_digit("box", house_num=5, digit=8))

    def test_find_cells_in_house_with_digit_possible(self):
        possible_3_keys_in_box_1 = {self.sudoku[key] for key in [(5, 0), (3, 1), (4, 1)]}
        self.assertEqual(
            possible_3_keys_in_box_1,
            self.sudoku.cells_in_house_with_digit_possible("box", house_num=1, digit=3)
        )

    def test_find_relevant_col_and_row(self):
        rectangle = {self.sudoku[k] for k in [(7, 1), (8, 1), (7, 2), (8, 2)]}
        relevant_col_num = 6
        relevant_row_num = 0
        self.assertEqual(relevant_row_num, find_empty_rectangle_house("row", rectangle))
        self.assertEqual(relevant_col_num, find_empty_rectangle_house("column", rectangle))

    def test_find_empty_rectangle_perp_SC_cells(self):
        relevant_row_num = 0
        relevant_col_num = 6
        expected = self.sudoku[5, 0]
        self.assertEqual(expected, self.solver.find_empty_rectangle_perp_sc_cell(relevant_row_num, relevant_col_num, digit=1))

class TestEmptyRectangleIntegration(unittest.TestCase):
    def setUp(self):
        unsolved = " 79 4 132" \
                   "14  739 6" \
                   "3  9 1 7 " \
                   "2    4 6 " \
                   "   7 6   " \
                   " 6   2 95" \
                   " 8   93 7" \
                   "73 4   19" \
                   "9 1 376  "
        self.sudoku = Sudoku.from_string(unsolved)
        edited = {
            (4, 2): {5},
            (1, 3): {5},
            (3, 3): {1},
            (4, 3): {1},
            (8, 3): {8},
            (1, 4): {5},
            (4, 4): {1},
            (8, 4): {4, 8},
            (2, 5): {8},
            (2, 6): {6},
            (4, 6): {6},
            (7, 6): {4},
            (2, 7): {5},
            (7, 8): {5}
        }
        self.sudoku.post_init(edited)
        self.solver = Solver(self.sudoku)

    def test_solver_clears_empty_rectangle(self):
        digit = 2
        cleared = self.sudoku[3, 8]
        self.assertTrue(self.solver.check_for_empty_rectangle())
        self.assertFalse(digit in cleared)


if __name__ == '__main__':
    unittest.main()
