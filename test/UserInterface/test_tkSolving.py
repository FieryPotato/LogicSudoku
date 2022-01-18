import unittest
from unittest.mock import patch

from src.GUI.Application import Application
from src.Sudoku import Sudoku


# @unittest.skip("Do not test unless testing GUI")
class testGUISolver(unittest.TestCase):
    def test_gui_is_connected_to_solver(self):
        app = Application()
        unsolved = Sudoku.from_string(
            "     3  9"
            " 795     "
            " 1 79  2 "
            "  6 2    "
            " 8   7 3 "
            "  3   8  "
            " 2   137 "
            "   8 619 "
            "         "
        )
        solved = Sudoku.from_string(
            "842613759"
            "679582413"
            "315794628"
            "756328941"
            "481967235"
            "293145867"
            "928451376"
            "534876192"
            "167239584"
        )
        started_full = {
            (5, 0), (8, 0), (1, 1), (2, 1), (3, 1), (1, 2), (3, 2), (4, 2), (7, 2),
            (2, 3), (4, 3), (1, 4), (5, 4), (7, 4), (2, 5), (6, 5), (1, 6), (5, 6),
            (6, 6), (7, 6), (3, 7), (5, 7), (6, 7), (7, 7)
        }
        for cell in solved:
            if cell.coordinates not in started_full:
                cell.started_empty = True
        app.sudoku.sudoku = unsolved
        self.assertFalse(app.sudoku.sudoku.is_complete)
        app.sudoku.solve()
        self.assertTrue(app.sudoku.sudoku.is_complete)
        self.assertTrue(app.sudoku.sudoku.is_legal())
        self.assertEqual(solved, app.sudoku.sudoku)

    def test_solver_load_solve_twice(self):
        unsolved_1 = '6    85  ' \
                     '  8 97  3' \
                     '  4 3  6 ' \
                     ' 7  43   ' \
                     ' 539 274 ' \
                     '   7   2 ' \
                     ' 1  8    ' \
                     '8  17 2  ' \
                     '  2   1 7'
        # unsolved_2 = "    7 5 3" \
        #              "4 8    1 " \
        #              "     289 " \
        #              " 4  957 8" \
        #              "  7 2 9  " \
        #              "8 5 4  2 " \
        #              "3 6      " \
        #              " 8 3   72" \
        #              "2 4 1    "
        sudokus = [Sudoku.from_string(unsolved_1) for _ in range(2)]
        with patch("src.GUI.Application.load_puzzle", side_effect=sudokus):
            app = Application()
            for _ in range(2):
                app.sudoku.new_sudoku()
                self.assertFalse(app.sudoku.is_complete)
                app.sudoku.solve()
                self.assertTrue(app.sudoku.is_complete)


if __name__ == "__main__":
    unittest.main()
