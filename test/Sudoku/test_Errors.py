import unittest

from src.Sudoku import Sudoku


class TestSudokuErrors(unittest.TestCase):
    def test_creating_sudoku_with_more_than_81_digits_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            invalid_str: str = " " * 82
            Sudoku.from_string(invalid_str)

    def test_creating_sudoku_with_fewer_than_81_digits_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            invalid_str: str = " " * 80
            Sudoku.from_string(invalid_str)

    def test_creating_sudoku_with_invalid_string_digits_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            invalid_str: str = "a" * 81
            Sudoku.from_string(invalid_str)

    def test_creating_sudoku_with_duplicates_in_row_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            double_row: str = "1       1" + (" " * 72)
            Sudoku.from_string(double_row)

    def test_creating_sudoku_with_duplicates_in_column_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            double_col: str = "1        " * 9
            Sudoku.from_string(double_col)

    def test_creating_sudoku_with_duplicates_in_box_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            double_box: str = "1         1       " + (" " * 63)
            Sudoku.from_string(double_box)