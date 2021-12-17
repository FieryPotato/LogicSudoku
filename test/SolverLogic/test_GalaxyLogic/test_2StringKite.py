import unittest

from src.Solver import Solver
from src.Sudoku import Sudoku


class Test_2StringKite_Methods(unittest.TestCase):
    test_str = "5 8 4    " \
               "427693158" \
               "3 6  84  " \
               "2 537 8  " \
               "87 264   " \
               "  3 852  " \
               "78    6 1" \
               " 528 674 " \
               "63     8 "

    strongly_connected_9_pair_keys = {
        ((1, 0), (1, 2)), ((0, 7), (0, 5)),  # columns
        ((3, 5), (0, 5)), ((8, 7), (0, 7)),  # rows
        ((2, 4), (0, 5)), ((5, 3), (3, 5)),  # boxes
    }

    strongly_connected_9_chain_keys = (
        [(2, 4), (0, 5), (0, 7), (8, 7)],
        [(2, 4), (0, 5), (3, 5), (5, 3)],
        [(8, 7), (0, 7), (0, 5), (3, 5), (5, 3)],
    )

    colour_chain_keys = [
        [
            [(2, 4), (0, 7)],
            [(0, 5), (8, 7)]
        ],
        [
            [(2, 4), (3, 5)],
            [(0, 5), (5, 3)]
        ],
        [
            [(8, 7), (0, 5), (5, 3)],
            [(0, 7), (3, 5)]
        ]
    ]

    def setUp(self) -> None:
        self.sudoku = Sudoku.from_string(self.test_str)
        edited = {
            (4, 2): {1},
            (1, 3): {1, 9},
            (1, 5): {1, 9},
            (7, 5): {1, 9},
            (8, 5): {9},
            (3, 8): {1, 5},
            (4, 8): {5},
            (5, 8): {1}
        }
        self.sudoku.post_init(edited)
        self.solver = Solver(self.sudoku)
        self.strongly_connected_9_pair_cells = {
            tuple(self.sudoku[key] for key in pair)
            for pair in self.strongly_connected_9_pair_keys
        }
        self.strongly_connected_chains = [
            [self.sudoku[key] for key in chain]
            for chain in self.strongly_connected_9_chain_keys
        ]
        self.colour_chains = [
            [
                [self.sudoku[key] for key in chain]
                for chain in pair]
            for pair in self.colour_chain_keys
        ]

    def test_find_strongly_connected_pairs_with_digit(self):
        digit = 9

        self.assertEqual(
            self.strongly_connected_9_pair_cells,
            self.solver.find_strongly_connected_pairs_with_digit(digit)
        )

    def test_find_strongly_connected_chains(self):
        self.assertEqual(
            self.strongly_connected_chains,
            strongly_connected_cell_chains(self.strongly_connected_9_pair_cells)
        )

    def test_isolate_colour_chains(self):
        self.assertEqual(
            self.colour_chains,
            colour_pairs_for_strongly_connected_chains(self.strongly_connected_chains)
        )

    def test_find_cells_seen_by_kite(self):
        seen_keys = {
            (1, 3), (8, 4), (1, 5), (4, 7), (8, 5), (7, 5),
        }
        seen_cells = {self.sudoku[key] for key in seen_keys}
        self.assertEqual(
            seen_cells,
            self.solver.cells_seen_by_colour_chains(self.colour_chains)
        )


class Test_2StringKite_Integration(unittest.TestCase):
    test_str = "    58   " \
               "5  3 12  " \
               " 8  4   5" \
               "49 7 3521" \
               "15 4    6" \
               " 2 1 5 94" \
               "7  51  6 " \
               "  58 4  9" \
               "    3  5 "

    edited = {
        (0, 0): {6},
        (1, 0): {6},
        (2, 0): {6, 7},
        (6, 0): {1, 3, 4, 7},
        (2, 1): {7},
        (4, 1): {6},
        (0, 2): {6},
        (2, 2): {6, 7},
        (3, 2): {7},
        (5, 2): {2, 9},
        (6, 2): {1, 3, 7},
        (4, 4): {8},
        (4, 7): {6},
        (7, 7): {1},
        (0, 8): {6},
        (1, 8): {6},
        (2, 8): {6},
        (3, 8): {2},
        (5, 8): {2, 9}
    }

    def setUp(self):
        self.sudoku = Sudoku.from_string(self.test_str)
        self.sudoku.post_init(self.edited)
        self.solver = Solver(self.sudoku)

    def test_solver_clears_2StringKite(self):
        digit = 7
        cell = self.sudoku[7, 7]

        self.assertTrue(self.solver.check_for_2_string_kite())

        self.assertFalse(digit in cell)


if __name__ == '__main__':
    unittest.main()
