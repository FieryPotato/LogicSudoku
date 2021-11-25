"""
Given three filled cells arranged in a rectangle and an empty cell that
completes that rectangle, if those filled cells started empty and the
two filled cells which are opposite each other have the same digit,
then the digit in the cell opposite the empty cell can be removed from
the empty cell's pencil marks.
"""

import unittest

from src.Sudoku import Sudoku
from src.Solver import Solver

UNSOLVED = " 629   43" \
           "93 461 5 " \
           "   23 6 9" \
           "   123968" \
           "6 95 4 3 " \
           "2 369 4 5" \
           "824356 9 " \
           " 7 849326" \
           "396712584"


class TestAvoidableRectangle(unittest.TestCase):
    def test_solver_clears_avoidable_rectangles(self):
        sudoku = Sudoku.from_string(UNSOLVED)
        started_filled = {(1, 0), (2, 0), (7, 0), (5, 1), (7, 1), (4, 2),
                          (6, 2), (8, 2), (4, 3), (6, 3), (8, 3), (3, 4),
                          (5, 4), (0, 5), (2, 5), (0, 6), (2, 6), (4, 6),
                          (1, 7), (3, 7), (4, 7), (7, 7), (1, 8), (3, 8),
                          (6, 8)}
        for cell in sudoku:
            if cell.coordinates not in started_filled:
                cell.started_empty = True
        solver = Solver(sudoku)
        avoidable_cell = sudoku[(7, 5)]
        avoidable_digit = 1

        self.assertTrue(solver.check_for_avoidable_rectangles())
        self.assertFalse(avoidable_digit in avoidable_cell.pencil_marks)


if __name__ == '__main__':
    unittest.main()
