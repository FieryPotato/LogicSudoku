import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


UNSOLVED_SAME = "92 743   " \
                "65 129   " \
                " 7 5682  " \
                "837914 2 " \
                "265387   " \
                "149256387" \
                "  2 3 8  " \
                "  687  32" \
                " 8  92 51"


class TestPointingRectangle(unittest.TestCase):
    def test_solver_clears_pointing_rectangle_with_pair_in_same_box(self):
        sudoku = Sudoku.from_string(UNSOLVED_SAME)
        solver = Solver(sudoku)

        edited = {
            (3, 0): {},
            (5, 0): {},
            (7, 0): {1},
            (0, 1): {},
            (2, 1): {4},
            (4, 1): {},
            (5, 1): {},
            (8, 1): {4},
            (1, 2): {},
            (3, 2): {},
            (4, 2): {},
            (7, 2): {4},
            (8, 2): {4},
            (2, 3): {},
            (4, 3): {},
            (5, 3): {},
            (7, 3): {},
            (0, 4): {},
            (1, 4): {},
            (2, 4): {},
            (0, 5): {},
            (2, 5): {},
            (3, 5): {},
            (4, 5): {},
            (6, 5): {},
            (7, 5): {},
            (4, 6): {},
            (7, 6): {4},
            (3, 7): {},
            (4, 7): {},
            (8, 7): {},
            (5, 8): {}
        }

        for key, pencil_marks in edited.items():
            cell = sudoku[key]
            cell.started_empty = True
            if pencil_marks:
                cell.remove(pencil_marks)

        affected_key = (7, 0)
        digit = {1}

        self.assertTrue(solver.check_for_pointing_rectangles())

        self.assertFalse(digit in sudoku[affected_key].pencil_marks)

    def test_solver_clears_pointing_rectangle_with_pair_in_two_boxes(self):
        pass


if __name__ == '__main__':
    unittest.main()
