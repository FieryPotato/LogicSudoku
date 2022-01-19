import json
import os
import unittest

from src.Sudoku import Sudoku


class TestSudokuMethods(unittest.TestCase):
    def test_sudoku_from_json(self):
        expected = Sudoku()
        fills = {
            (1, 1): 1,
            (4, 1): 2,
            (7, 1): 3,
            (1, 4): 4,
            (4, 4): 5,
            (7, 4): 6,
            (1, 7): 7,
            (4, 7): 8,
            (7, 7): 9
        }
        edited = {
            (8, 8): {1, 2, 3, 4, 5, 6, 7}
        }
        for k, v in fills.items():
            expected[k].fill(v)
            expected[k].started_empty = False
        expected.post_init(edited)

        test_file_location = os.path.join("test", "Sudoku", "test_from_json.json")

        with open(test_file_location, "r") as file:
            data = json.load(file)
        actual = Sudoku.from_json(data)

        self.assertEqual(expected, actual)
        self.assertTrue(actual[7, 8].started_empty)

    def test_sudoku_from_text_file(self):
        expected = Sudoku()
        fills = {
            (1, 1): 1,
            (4, 1): 2,
            (7, 1): 3,
            (1, 4): 4,
            (4, 4): 5,
            (7, 4): 6,
            (1, 7): 7,
            (4, 7): 8,
            (7, 7): 9
        }

        for k, v in fills.items():
            expected[k].fill(v)
            expected[k].started_empty = False
        expected.update_pencil_marks()

        test_file_location = os.path.join("test", "Sudoku", "test_from_txt.txt")

        with open(test_file_location, "r") as file:
            data = file.read()
        actual = Sudoku.from_string(data)

        self.assertEqual(expected, actual)

    def test_sudoku_can_be_filled_with_digits_after_init(self):
        sudoku = Sudoku()
        x, y, digit = 4, 4, 4
        sudoku.fill(x, y, digit)
        self.assertEqual(digit, sudoku[x, y].digit)

    def test_filling_illegal_digits_raises_value_error(self):
        sudoku = Sudoku.from_string(
            "1        "
            "         "
            "         "
            "         "
            "         "
            "         "
            "         "
            "         "
            "         "
        )
        x, y, digit = 1, 1, 1
        sudoku.fill(x, y, digit)
        self.assertNotEqual(digit, sudoku[x, y].digit)

    def test_clearing_sudoku_cell_resets_it(self):
        sudoku = Sudoku.from_string(
            "         "
            "         "
            "         "
            "         "
            "         "
            "         "
            "         "
            "         "
            "         "
        )
        x, y, digit = 1, 2, 3
        sudoku.fill(x, y, digit)
        sudoku.clear(x, y)
        self.assertTrue(sudoku[x, y].is_empty)


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

    def test_columns_property(self) -> None:
        col_keys = [col for col in self.columns]
        actual_cols: list = [[cell.coordinates for cell in column] for column in self.sudoku.columns]
        self.assertEqual(col_keys, actual_cols)


if __name__ == "__main__":
    unittest.main()