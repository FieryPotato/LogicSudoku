import unittest
from copy import deepcopy

from src.Cell import Cell
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
    b_1 = [(0, 0), (1, 0), (2, 0),
           (0, 1), (1, 1), (2, 1),
           (0, 2), (1, 2), (2, 2)]
    b_2 = [(3, 0), (4, 0), (5, 0),
           (3, 1), (4, 1), (5, 1),
           (3, 2), (4, 2), (5, 2)]
    b_3 = [(6, 0), (7, 0), (8, 0),
           (6, 1), (7, 1), (8, 1),
           (6, 2), (7, 2), (8, 2)]
    b_4 = [(0, 3), (1, 3), (2, 3),
           (0, 4), (1, 4), (2, 4),
           (0, 5), (1, 5), (2, 5)]
    b_5 = [(3, 3), (4, 3), (5, 3),
           (3, 4), (4, 4), (5, 4),
           (3, 5), (4, 5), (5, 5)]
    b_6 = [(6, 3), (7, 3), (8, 3),
           (6, 4), (7, 4), (8, 4),
           (6, 5), (7, 5), (8, 5)]
    b_7 = [(0, 6), (1, 6), (2, 6),
           (0, 7), (1, 7), (2, 7),
           (0, 8), (1, 8), (2, 8)]
    b_8 = [(3, 6), (4, 6), (5, 6),
           (3, 7), (4, 7), (5, 7),
           (3, 8), (4, 8), (5, 8)]
    b_9 = [(6, 6), (7, 6), (8, 6),
           (6, 7), (7, 7), (8, 7),
           (6, 8), (7, 8), (8, 8)]
    box_keys = [b_1, b_2, b_3, b_4, b_5, b_6, b_7, b_8, b_9]

    def test_sudoku_boxes_individually(self) -> None:
        sudoku: Sudoku = Sudoku()

        for i, expected_keys in enumerate(self.box_keys):
            actual_keys: list[tuple[int, int]] = [cell.coordinates for cell in sudoku.box(i)]
            self.assertEqual(expected_keys, actual_keys)

    def test_boxes_property(self) -> None:
        sudoku: Sudoku = Sudoku()
        actual_boxes: list = [[cell.coordinates for cell in box] for box in sudoku.boxes]
        self.assertEqual(self.box_keys, actual_boxes)


if __name__ == '__main__':
    unittest.main()
