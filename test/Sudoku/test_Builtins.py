import unittest
from copy import deepcopy

from src.Sudoku import Sudoku


class TestSudokuBuiltins(unittest.TestCase):
    def test_changing_pencil_marks_causes_sudoku_equality_to_fail(self) -> None:
        a: Sudoku = Sudoku.from_string(" " * 81)
        b: Sudoku = deepcopy(a)
        self.assertEqual(a, b)
        a[(0, 0)].pencil_marks = {1}
        self.assertNotEqual(a, b)