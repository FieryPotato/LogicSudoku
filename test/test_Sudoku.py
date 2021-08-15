import unittest

from src.Sudoku import Sudoku


class TestSudoku(unittest.TestCase):
    def test_creating_sudoku_with_more_than_81_digits_raises_value_error(self):
        with self.assertRaises(ValueError):
            invalid_str = " " * 82
            Sudoku.from_string(invalid_str)

    def test_creating_sudoku_with_fewer_than_81_digits_raises_value_error(self):
        with self.assertRaises(ValueError):
            invalid_str = " " * 80
            Sudoku.from_string(invalid_str)


if __name__ == '__main__':
    unittest.main()
