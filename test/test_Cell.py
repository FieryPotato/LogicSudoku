import unittest

from src.Sudoku import BOX_MAP, Sudoku


class TestCell(unittest.TestCase):
    def test_box_num(self):
        sudoku = Sudoku()
        for key, box in BOX_MAP.items():
            for cell in box:
                self.assertEqual(sudoku[cell].box_num, key)


if __name__ == '__main__':
    unittest.main()
