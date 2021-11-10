"""
If three cells meet the following criteria:
- Cells A, B, and C each contain only 2 possible options;
- Cells A, B, and C share exactly one option with each of the others;
    - i.e. pencil marks are A: x, y; B: y, z; C: x, z.
- Cell A sees each of B and C, but B and C do not see each other;

Then cells which see both B and C can have z cleared from their options.
"""


import unittest

from src.Sudoku import Sudoku
from src.Solver import Solver


UNSOLVED_1 = " 78 2  9 " \
             " 29 876  " \
             "461953872" \
             "74  68   " \
             "216579348" \
             "    417 6" \
             "1 27    5" \
             "  4 152 7" \
             " 57  21  "


class TestYWing(unittest.TestCase):
    def test_solver_clears_ywings(self):
        sudoku = Sudoku.from_string(UNSOLVED_1)
        solver = Solver(sudoku)
        cleared_cells = {(6, 0), (0, 1)}
        cleared_digit = 5

        sudoku[(8, 0)].pencil_marks.remove(4)
        sudoku[(7, 1)].pencil_marks.remove(3)

        self.assertTrue(solver.check_for_ywings())

        for key in cleared_cells:
            self.assertFalse(cleared_digit in sudoku[key].pencil_marks)


if __name__ == '__main__':
    unittest.main()
