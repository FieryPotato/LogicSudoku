import unittest

from src.Cell import Cell
from src.Sudoku import Sudoku, BOX_MAP


class TestCell(unittest.TestCase):
    def setUp(self) -> None:
        self.sudoku = Sudoku()

    def test_box_num(self):
        for key, box in BOX_MAP.items():
            for cell in box:
                self.assertEqual(self.sudoku[cell].box_num, key)

    def test_visible_cells(self):
        test = self.sudoku[(0, 0)]
        column = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)}
        row = {(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0)}
        box = {(1, 0), (2, 0), (0, 1), (1, 1), (1, 2), (0, 2), (2, 1), (2, 2)}
        all_groups = set.union(*[column, row, box])
        self.assertEqual(column, test.visible_cells("column"))
        self.assertEqual(row, test.visible_cells("row"))
        self.assertEqual(box, test.visible_cells("box"))
        self.assertEqual(all_groups, test.visible_cells())

    def test_sees(self):
        test_keys = [(0, 0), (0, 4), (4, 0), (4, 4), (7, 7), (8, 6)]
        test_cells = [self.sudoku[key] for key in test_keys]
        a, b, c, d, e, f = test_cells
        true_pairs = (a, b), (a, c), (b, d), (c, d), (e, f)
        false_pairs = ((a, d), (b, c), (a, e), (a, f), (b, e),
                       (b, f), (c, e), (c, f), (d, e), (d, f))
        for x, y in true_pairs:
            self.assertTrue(x.sees(y))
            self.assertTrue(y.sees(x))
        for x, y in false_pairs:
            self.assertFalse(x.sees(y))
            self.assertFalse(y.sees(x))

    def test_cells_do_not_see_themselves(self):
        for cell in self.sudoku:
            self.assertFalse(cell.sees(self.sudoku[cell.coordinates]))

    def test_intersection(self):
        a = (0, 0)
        b = (2, 2)
        c = (8, 0)
        d = (6, 2)
        tests = {
            (a, b, c): {(1, 0), (2, 0)},
            (b, c, d): {(7, 2), (8, 2)},
            (a, d): {(0, 2), (1, 2), (2, 2), (6, 0), (7, 0), (8, 0)},
            (a, c): {(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)}
        }

        for test_keys, expected in tests.items():
            test = [Cell(key) for key in test_keys]
            self.assertEqual(expected, Cell.intersection(*test))
            self.assertEqual(expected, test[0].intersection(*test[1:]))