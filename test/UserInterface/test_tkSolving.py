import unittest

from src.GUI.Application import Application
from src.Sudoku import Sudoku


@unittest.skip("Do not test unless testing GUI")
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
        app.sudoku.sudoku = unsolved
        self.assertFalse(app.sudoku.sudoku.is_complete)
        app.sudoku.solve()
        self.assertTrue(app.sudoku.sudoku.is_complete)
        self.assertTrue(app.sudoku.sudoku.is_legal())
        self.assertEqual(solved, app.sudoku.sudoku)


if __name__ == "__main__":
    unittest.main()
