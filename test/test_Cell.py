import unittest

from src.Sudoku import BOX_MAP, Sudoku


class TestCell(unittest.TestCase):
    def setUp(self) -> None:
        self.sudoku = Sudoku()

    def test_box_num(self):
        for key, box in BOX_MAP.items():
            for cell in box:
                self.assertEqual(self.sudoku[cell].box_num, key)

    def test_visible_cells(self):
        test = self.sudoku[(0, 0)]
        expected = {(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8),  # cells in column
                      (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0),  # cells in row
                      (1, 1), (1, 2), (2, 1), (2, 2)}                                  # cells in box
        self.assertEqual(expected, test.visible_cells)

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


if __name__ == '__main__':
    unittest.main()
