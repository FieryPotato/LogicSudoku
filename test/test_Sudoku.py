import unittest
from copy import deepcopy

from src.Sudoku import Sudoku


class TestSudoku(unittest.TestCase):
    def test_creating_sudoku_with_more_than_81_digits_raises_value_error(self):
        with self.assertRaises(ValueError):
            invalid_str: str = " " * 82
            Sudoku.from_string(invalid_str)

    def test_creating_sudoku_with_fewer_than_81_digits_raises_value_error(self):
        with self.assertRaises(ValueError):
            invalid_str: str = " " * 80
            Sudoku.from_string(invalid_str)

    def test_changing_pencil_marks_causes_sudoku_equality_to_fail(self):
        a: Sudoku = Sudoku.from_string(" " * 81)
        b: Sudoku = deepcopy(a)
        self.assertEqual(a, b)
        a[(0, 0)].pencil_marks = {1}
        self.assertNotEqual(a, b)


if __name__ == '__main__':
    unittest.main()
