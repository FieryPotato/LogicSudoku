import unittest
from copy import deepcopy

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

    def test_creating_sudoku_with_invalid_string_digits(self) -> None:
        with self.assertRaises(ValueError):
            invalid_str: str = "a" * 81
            Sudoku.from_string(invalid_str)


class TestSudokuBuiltins(unittest.TestCase):
    def test_changing_pencil_marks_causes_sudoku_equality_to_fail(self) -> None:
        a: Sudoku = Sudoku.from_string(" " * 81)
        b: Sudoku = deepcopy(a)
        self.assertEqual(a, b)
        a[(0, 0)].pencil_marks = {1}
        self.assertNotEqual(a, b)


class TestSudokuProperties(unittest.TestCase):
    boxes = {1: [(0, 0), (1, 0), (2, 0),
                 (0, 1), (1, 1), (2, 1),
                 (0, 2), (1, 2), (2, 2)],
             2: [(3, 0), (4, 0), (5, 0),
                 (3, 1), (4, 1), (5, 1),
                 (3, 2), (4, 2), (5, 2)],
             3: [(6, 0), (7, 0), (8, 0),
                 (6, 1), (7, 1), (8, 1),
                 (6, 2), (7, 2), (8, 2)],
             4: [(0, 3), (1, 3), (2, 3),
                 (0, 4), (1, 4), (2, 4),
                 (0, 5), (1, 5), (2, 5)],
             5: [(3, 3), (4, 3), (5, 3),
                 (3, 4), (4, 4), (5, 4),
                 (3, 5), (4, 5), (5, 5)],
             6: [(6, 3), (7, 3), (8, 3),
                 (6, 4), (7, 4), (8, 4),
                 (6, 5), (7, 5), (8, 5)],
             7: [(0, 6), (1, 6), (2, 6),
                 (0, 7), (1, 7), (2, 7),
                 (0, 8), (1, 8), (2, 8)],
             8: [(3, 6), (4, 6), (5, 6),
                 (3, 7), (4, 7), (5, 7),
                 (3, 8), (4, 8), (5, 8)],
             9: [(6, 6), (7, 6), (8, 6),
                 (6, 7), (7, 7), (8, 7),
                 (6, 8), (7, 8), (8, 8)]}
    box_keys = [box_list for box_list in boxes.values()]
    rows = [[(j, i) for j in range(9)] for i in range(9)]
    columns = [[(i, j) for j in range(9)] for i in range(9)]

    def setUp(self) -> None:
        self.sudoku: Sudoku = Sudoku()

    def test_boxes_individually(self) -> None:
        for i, expected_keys in enumerate(self.box_keys):
            actual_keys: list[tuple[int, int]] = [cell.coordinates for cell in self.sudoku.box(i)]
            self.assertEqual(expected_keys, actual_keys)

    def test_boxes_property(self) -> None:
        actual_boxes: list = [[cell.coordinates for cell in box] for box in self.sudoku.boxes]
        self.assertEqual(self.box_keys, actual_boxes)

    def test_rows_individually(self) -> None:
        for i, expected_keys in enumerate(self.rows):
            actual_keys: list[tuple[int, int]] = [cell.coordinates for cell in self.sudoku.row(i)]
            self.assertEqual(expected_keys, actual_keys)

    def test_rows_property(self) -> None:
        row_keys = [row for row in self.rows]
        actual_rows: list = [[cell.coordinates for cell in row] for row in self.sudoku.rows]
        self.assertEqual(row_keys, actual_rows)

    def test_columns_individually(self) -> None:
        for i, expected_keys in enumerate(self.columns):
            actual_keys: list[tuple[int, int]] = [cell.coordinates for cell in self.sudoku.column(i)]
            self.assertEqual(expected_keys, actual_keys)

    def tesT_columns_property(self) -> None:
        col_keys = [col for col in self.columns]
        actual_cols: list = [[cell.coordinates for cell in column] for column in self.sudoku.columns]
        self.assertEqual((col_keys, actual_cols))


if __name__ == '__main__':
    unittest.main()
