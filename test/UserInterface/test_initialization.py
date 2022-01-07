import unittest
from unittest.mock import patch

from src.GUI.tkinter import App
from src.Sudoku import Sudoku


class TestLoadingSudoku(unittest.TestCase):
    def test_loading_from_string(self):
        expected = Sudoku.from_string(
            "1        "
            " 2       "
            "  3      "
            "   4     "
            "    5    "
            "     6   "
            "      7  "
            "       8 "
            "        9"
        )
        mock = "test/UserInterface/mock_files/initialization_LoadingSudoku_LoadingFromString_with_linebreaks.txt"
        with patch("tkinter.filedialog.askopenfilename",
                   return_value=mock):
            app = App()
            actual = app.load_puzzle()
            self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()
