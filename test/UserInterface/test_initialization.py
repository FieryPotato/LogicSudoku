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
        mock = "test/UserInterface/mock_files/initialization_LoadingSudoku_LoadingFromString.txt"
        with patch("tkinter.filedialog.askopenfilename", return_value=mock):
            app = App()
            actual = app.load_puzzle()
            self.assertEqual(expected, actual)

    def test_loading_from_json(self):
        expected = Sudoku.from_json(
            {
                "cells":
                    {
                        "(0, 8)": 1,
                        "(1, 7)": 2,
                        "(2, 6)": 3,
                        "(3, 5)": 4,
                        "(4, 4)": 5,
                        "(5, 3)": 6,
                        "(6, 2)": 7,
                        "(7, 1)": 8,
                        "(8, 0)": 9
                    },
                "pencil marks":
                    {
                        "(0, 0)": [1, 2, 3],
                        "(8, 8)": [7, 8, 9]
                    }
            }
        )
        mock = "test/UserInterface/mock_files/initialization_LoadingSudoku_LoadingFromJSON.json"
        with patch("tkinter.filedialog.askopenfilename", return_value=mock):
            app = App()
            actual = app.load_puzzle()
            self.assertEqual(expected, actual)

    def test_loading_other_file_type_raises_value_error(self):
        mock = "test/UserInterface/mock_files/initialization_LoadingSudoku_InvalidFileType.jpg"
        with patch("tkinter.filedialog.askopenfilename", return_value=mock):
            app = App()
            self.assertRaises(ValueError, app.load_puzzle)


if __name__ == '__main__':
    unittest.main()
