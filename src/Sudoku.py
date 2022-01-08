from itertools import product, combinations, permutations
from typing import ItemsView, KeysView, Iterator, Generator, Iterable

from src.Cell import Cell

RCB_ITER = "rows", "columns", "boxes"
CELL_KEYS: list = [(j, i) for i, j in product(range(9), repeat=2)]
BOX_MAP: dict = {
    0: ((0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
        (0, 2), (1, 2), (2, 2)),
    1: ((3, 0), (4, 0), (5, 0),
        (3, 1), (4, 1), (5, 1),
        (3, 2), (4, 2), (5, 2)),
    2: ((6, 0), (7, 0), (8, 0),
        (6, 1), (7, 1), (8, 1),
        (6, 2), (7, 2), (8, 2)),
    3: ((0, 3), (1, 3), (2, 3),
        (0, 4), (1, 4), (2, 4),
        (0, 5), (1, 5), (2, 5)),
    4: ((3, 3), (4, 3), (5, 3),
        (3, 4), (4, 4), (5, 4),
        (3, 5), (4, 5), (5, 5)),
    5: ((6, 3), (7, 3), (8, 3),
        (6, 4), (7, 4), (8, 4),
        (6, 5), (7, 5), (8, 5)),
    6: ((0, 6), (1, 6), (2, 6),
        (0, 7), (1, 7), (2, 7),
        (0, 8), (1, 8), (2, 8)),
    7: ((3, 6), (4, 6), (5, 6),
        (3, 7), (4, 7), (5, 7),
        (3, 8), (4, 8), (5, 8)),
    8: ((6, 6), (7, 6), (8, 6),
        (6, 7), (7, 7), (8, 7),
        (6, 8), (7, 8), (8, 8))
}

# Van De Wetering Squares
vdw_map = {
    "top": {
        "keys": [(4, 0), (4, 1), (4, 2), (4, 3)],
        "parity": 2

    },
    "bottom": {
        "keys": [(4, 5), (4, 6), (4, 7), (4, 8)],
        "parity": 3
    },
    "left": {
        "keys": [(0, 4), (1, 4), (2, 4), (3, 4)],
        "parity": 5
    },
    "right": {
        "keys": [(5, 4), (6, 4), (7, 4), (8, 4)],
        "parity": 7
    }
}
vdw_even_inner_keys = [[(3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3)],
                       [(8, 5), (7, 5), (6, 5), (5, 5), (5, 6), (5, 7), (5, 8)]]
vdw_odd_inner_keys = [[(5, 0), (5, 1), (5, 2), (5, 3), (6, 3), (7, 3), (8, 3)],
                      [(0, 5), (1, 5), (2, 5), (3, 5), (3, 6), (3, 7), (3, 8)]]
vdw_key_map = {
    10: vdw_even_inner_keys,
    14: vdw_odd_inner_keys,
    15: vdw_odd_inner_keys,
    21: vdw_even_inner_keys,
}
vdw_index_map = {
    10: 0,
    14: 0,
    15: 1,
    21: 1
}


class Sudoku:
    def __init__(self) -> None:
        self.cell_dict = {k: Cell(k) for k in CELL_KEYS}

    def __str__(self) -> str:
        blank = "{}{}{}|{}{}{}|{}{}{}\n" \
                "{}{}{}|{}{}{}|{}{}{}\n" \
                "{}{}{}|{}{}{}|{}{}{}\n" \
                "-----------\n" \
                "{}{}{}|{}{}{}|{}{}{}\n" \
                "{}{}{}|{}{}{}|{}{}{}\n" \
                "{}{}{}|{}{}{}|{}{}{}\n" \
                "-----------\n" \
                "{}{}{}|{}{}{}|{}{}{}\n" \
                "{}{}{}|{}{}{}|{}{}{}\n" \
                "{}{}{}|{}{}{}|{}{}{}\n"
        values = [self.cell_dict[k].digit for k in CELL_KEYS]
        return blank.format(*values)

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            if self.cell_dict == other.cell_dict:
                return True
        return False

    def __ne__(self, other) -> bool:
        if isinstance(other, self.__class__):
            if self.cell_dict == other.cell_dict:
                return False
        return True

    def __setitem__(self, key, value) -> None:
        if key not in self.cell_dict:
            raise KeyError(f"{key} is not a valid cell key.")
        self.cell_dict[key] = value
        return None

    def __getitem__(self, *args) -> Cell:
        if len(args) == 1:
            return self.cell_dict[args[0]]
        elif len(args) == 2:
            return self.cell_dict[args]
        else:
            raise KeyError(f"{args} is not a valid cell key.")

    def __delitem__(self, key) -> None:
        if key not in self.cell_dict:
            raise KeyError(f"{key} is not a valid cell key.")
        self.cell_dict[key].clear()
        return None

    def __iter__(self) -> Iterator[Cell]:
        """Iterate over cell objects in the sudoku in the following order of keys:
        (0, 0), (1, 0), (2, 0), ... (8, 0), (0, 1), (1, 1), ... (8, 8)"""
        for key in CELL_KEYS:
            yield self[key]

    @property
    def is_complete(self) -> bool:
        """Return whether the sudoku has empty cells."""
        for cell in self:
            if cell.is_empty:
                return False
        return True

    def is_legal(self, return_cell=False) -> bool | tuple[int, int]:
        """Return false if the sudoku has any duplicate digits in rows,
        columns, or boxes."""
        present_digits = set()
        for house_type in "rows", "columns", "boxes":
            for house in getattr(self, house_type):
                for cell in house:
                    if not cell.is_empty:
                        if cell.digit in present_digits:
                            if return_cell is True:
                                return cell.coordinates
                            return False
                        present_digits.add(cell.digit)
                present_digits.clear()
        return True

    @property
    def rows(self) -> Iterator[list[Cell]]:
        """Generate rows in the sudoku for iteration."""
        yield from [self.row(i) for i in range(9)]

    @property
    def columns(self) -> Iterator[list[Cell]]:
        """Generate columns in the sudoku for iteration."""
        yield from [self.column(i) for i in range(9)]

    @property
    def boxes(self) -> Iterator[list[Cell]]:
        """Generate boxes in the sudoku for iteration."""
        yield from [self.box(i) for i in range(9)]

    def items(self) -> ItemsView:
        """Return an ItemsView of (key, cell) pairs in the Sudoku."""
        return self.cell_dict.items()

    def keys(self) -> KeysView:
        """Return the KeysView of the sudoku in
        (0, 0), (1, 0), (2, 0), ... (8, 0), (0, 1), (1, 1), ... (8, 8)
        order."""
        return self.cell_dict.keys()

    def set_cell(self, coordinates, value) -> None:
        """Set the chosen cell's value."""
        self[coordinates].fill(value)
        return None

    def get_cell(self, coordinates) -> int | str:
        """Return the digit in input coordinates' cell."""
        return self[coordinates].digit

    def check_cell_pencil_marks(self, coordinates) -> None:
        """Clear pencil marks from a cell if the pencil mark appears
        in the cell's row, column, or box."""
        cell: Cell = self[coordinates]
        if cell.is_empty:
            row_digits: set = {self[c].digit for c in cell.row}
            column_digits: set = {self[c].digit for c in cell.column}
            box_digits: set = {self[c].digit for c in cell.box}
            invalid_digits: set = row_digits.union(column_digits, box_digits)
            cell.pencil_marks -= invalid_digits
        else:
            cell.pencil_marks = set()

    def update_pencil_marks(self) -> None:
        """Update all pencil marks in the puzzle based only on cell/row/box
         logic."""
        for key in self.keys():
            self.check_cell_pencil_marks(key)

    def box(self, b) -> list[Cell]:
        """Return the list of cells in box top_right of the Sudoku."""
        return [self[cell] for cell in BOX_MAP[b]]

    def row(self, r) -> list[Cell]:
        """Return the list of cells in row r of the Sudoku."""
        return [self[key] for key in [(c, r) for c in range(9)]]

    def column(self, c) -> list[Cell]:
        """Return the list of cells in column bot_left """
        return [self[key] for key in [(c, r) for r in range(9)]]

    def post_init(self, edited_cells: dict[tuple[int, int], [set[int]]]) -> None:
        """Set self.cells that are keys of edited_cells to have started empty
        and remove digits in sets that are values of edited_cells from those
        cells' pencil_marks. Mainly for use in testing.

        :param edited_cells: e.g. (1, 1): set() or (2, 2): {1, 5, 9}
        """
        for key, digits in edited_cells.items():
            if digits == {}:
                digits = set()
            self[key].pencil_marks -= digits
            self[key].started_empty = True
        self.update_pencil_marks()

    def rectangles(self) -> Generator[tuple[Cell, Cell, Cell, Cell], None, None]:
        """Yield cells arranged in a rectangle."""
        for row in self.rows:
            for top_left, top_right in combinations(row, r=2):
                for bottom_left in [self[key]
                                    for key in top_left.visible_cells("column")
                                    if key[1] > top_left.y]:
                    bottom_right = self[top_right.x, bottom_left.y]
                    yield top_left, top_right, bottom_left, bottom_right

    @staticmethod
    def house_contains_filled_digit(digit: int, house: list[Cell]) -> bool:
        """Return whether input house of self contains input digit."""
        house_digits = {cell.digit for cell in house if not cell.is_empty}
        return digit in house_digits

    def houses_with_digit(self, house_type: str, digit: int) -> Generator[list[Cell], None, None]:
        iter_house_type = house_type + "s"
        for house in getattr(self, iter_house_type):
            if len([cell for cell in house if digit in cell]):
                yield house

    @classmethod
    def from_string(cls, string: str, edited: dict = None) -> "Sudoku":
        """
        Return a sudoku whose cells in order appear in an 81-character
        string. Spaces mark empty cells, and the \n character can be
        used to break up lines for ease of formatting.

        If edited is supplied, then for each key in edited, remove all
        digits in edited[key] from sudoku[key].
        """
        string = string.replace("\n", "")
        if len(string) < 81:
            raise ValueError("Your sudoku contains fewer than 81 digits.")
        elif len(string) > 81:
            raise ValueError("Your sudoku contains more than 81 digits.")
        new = cls()
        for i, key in enumerate(CELL_KEYS):
            digit = string[i]
            cell = new[key]
            cell.fill(digit)
            cell.started_empty = False
        if not new.is_legal():
            coordinates = new.is_legal(return_cell=True)
            raise ValueError(f"Your sudoku contains a duplicate at {coordinates}.")
        if edited is not None:
            new.post_init(edited)
        return new

    @classmethod
    def from_json(cls, data) -> "Sudoku":
        """
        Construct and return a sudoku from a json data structure. The
        data should have the following character:

        {
            "cells": {
                ([key; eg. 0, 0]): [int in range(1, 10)],
                etc.
            },
            "pencil marks": {
                ([key]): [[list of ints in range(1, 10)]],
                etc.
            }
        }

        Key, value pairs in "cells" fill the cells in sudoku at those
        keys with value. Key, value pairs in "pencil marks" remove the
        digits in value from the cell at key.

        If loading from file, keys should be strings that eval() to
        tuples that contain two ints, eg.: "(6, 9)".
        """
        new = cls()
        if "cells" in data:
            cell_dict: dict = data["cells"]
            for k, v in cell_dict.items():
                key = eval(k)
                value = Cell(key)
                digit = v
                value.fill(digit)
                new.cell_dict[key] = value
            for cell in new:
                if not cell.is_empty:
                    cell.started_empty = False
        if "pencil marks" in data:
            pencil_marks_data = data["pencil marks"]
            new_pencil_marks = {eval(k): set(v) for k, v in pencil_marks_data.items()}
            new.post_init(new_pencil_marks)
        new.update_pencil_marks()
        return new

    def phistomephel_sets(self, left_col: int = None, right_col: int = None,
                          top_row: int = None, bot_row: int = None) -> \
            list[tuple[set[Cell], set[Cell]]] | tuple[set[Cell], set[Cell]]:
        """
        Return a list of pairs of sets that are a consequence of
        Phistomephel's Theorem. If no params are None, then instead
        just return a pair of sets where the ring is determined by the
        params. The famous ring would be generated by
        >>> Sudoku.phistomephel_sets(left_col=2, right_col=6, top_row=2, bot_row=6)

        :param left_col: column 0, 1, 2: int in range(3) or None
        :param right_col: column 6, 7, 8: int in range(6, 9) or None
        :param top_row: row 0, 1, 2: int in range(3) or None
        :param bot_row: row 6, 7, 8: int in range(6, 9) or None
        :return: Two sets containing identical digits if no params are None, otherwise return a list of such sets.
        """
        if min([isinstance(param, int) for param in (left_col, right_col, top_row, bot_row)]):
            return self.single_phistomephel_set(left_col, right_col, top_row, bot_row)

        lc = [left_col] if left_col is not None else range(3)
        rc = [right_col] if right_col is not None else range(6, 9)
        tr = [top_row] if top_row is not None else range(3)
        br = [bot_row] if bot_row is not None else range(6, 9)

        sets = []
        for a, b, c, d in product(
                [i for i in lc],
                [i for i in rc],
                [i for i in tr],
                [i for i in br]
        ):
            sets.append(self.single_phistomephel_set(a, b, c, d))

        return sets

    def single_phistomephel_set(self, left_col: int, right_col: int, top_row: int, bot_row: int) \
            -> tuple[set[Cell], set[Cell]]:
        box_0 = {cell for cell in self.box(0)
                 if cell not in self.row(top_row)
                 and cell not in self.column(left_col)}
        box_2 = {cell for cell in self.box(2)
                 if cell not in self.row(top_row)
                 and cell not in self.column(right_col)}
        box_6 = {cell for cell in self.box(6)
                 if cell not in self.row(bot_row)
                 and cell not in self.column(left_col)}
        box_8 = {cell for cell in self.box(8)
                 if cell not in self.row(bot_row)
                 and cell not in self.column(right_col)}

        box_1 = {cell for cell in self.row(top_row)
                 if cell in self.box(1)}
        box_3 = {cell for cell in self.column(left_col)
                 if cell in self.box(3)}
        box_5 = {cell for cell in self.column(right_col)
                 if cell in self.box(5)}
        box_7 = {cell for cell in self.row(bot_row)
                 if cell in self.box(7)}
        box_9 = {self[k]
                 for k in ((left_col, top_row), (right_col, top_row),
                           (left_col, bot_row), (right_col, bot_row))}

        corners = set.union(box_0, box_2, box_6, box_8)
        ring = set.union(box_1, box_3, box_5, box_7, box_9)

        return corners, ring

    @staticmethod
    def cells_share_a_row(*cells: Cell) -> bool:
        return len({cell.y for cell in cells}) == 1

    @staticmethod
    def cells_share_a_column(*cells: Cell) -> bool:
        return len({cell.x for cell in cells}) == 1

    @staticmethod
    def cells_share_a_box(*cells: Cell) -> bool:
        return len({cell.box_num for cell in cells}) == 1

    @staticmethod
    def cells_form_a_rectangle(*cells: Cell) -> bool:
        """Return whether input cells form a rectangle."""
        if len(cells) != 4: return False
        for order in permutations(cells, r=4):
            a, b, c, d = order
            if a.x == c.x and a.y == b.y and d.x == b.x and d.y == c.y:
                return True
        return False

    @staticmethod
    def cells_in_group_with_digits(digits: Iterable[int], group: list[Cell]):
        """
        Return a list of cells in input house that contain each digit in
        digits.
        """
        empty_cells = {cell for cell in group if cell.is_empty}
        cells_with_digits = [
            {cell for cell in empty_cells if digit in cell} for digit in digits
        ]
        flattened_cells = {cell for _list in cells_with_digits for cell in _list}
        return flattened_cells

    def cells_share_same_house(self, house_type, *cells) -> bool:
        """
        Return whether cells share a row or column.

        A helper function that allows iteration over houses; c.f.
        Solver.cells_share_opposite_house.
        """
        if house_type == "row":
            return self.cells_share_a_row(*cells)
        elif house_type == "column":
            return self.cells_share_a_column(*cells)
        else:
            raise ValueError(f"{house_type} is not a valid argument for"
                             f" Solver.cells_share_same_house.")

    def cells_share_opposite_house(self, house_type, *cells) -> bool:
        """
        Return whether cells share a row or column opposite the input group.

        A helper function that allows iteration over houses; c.f.
        Solver.cells_share_same_house.
        """
        if house_type == "row":
            return self.cells_share_a_column(*cells)
        elif house_type == "column":
            return self.cells_share_a_row(*cells)
        else:
            raise ValueError(f"{house_type} is not a valid argument for"
                             f"Solver.cells_share_opposite_house.")

    def strongly_connected_pairs_with_digit(self, digit: int) -> set[tuple[Cell, Cell]]:
        """
        Return a set containing tuples of cells which are strongly
        connected by digit.
        """
        pairs = []
        for house_type in RCB_ITER:
            for house in getattr(self, house_type):
                cells_with_digit = {cell for cell in house if digit in cell}
                if len(cells_with_digit) == 2:
                    pairs.append(tuple(cells_with_digit))
        return set(pairs)

    def single_vdw_square(self, vertical: str, horizontal: str) -> tuple[set[Cell], set[Cell]]:
        """
        Aad Van De Wetering proved that if you take the first 5
        columns in a sudoku as a set and compare them to the bottom 4
        rows, the 5 columns contain identical digits to the digits in
        the rows plus one set of the digits 1–9 (obviously). The non-
        trivial extension of this is to have all cells that appear in
        both sets cancel each other out, such that we have two opposed
        v-shapes in opposite corners of the sudoku, one of which is one
        square thick and the other two squares. These v's also share
        the relation of being equal to the other plus one complete set
        of the digits 1-9.

        :param vertical: "top" or "bottom"
        :param horizontal: "left" or "right"
        :return: {large square set}, {small square set}
        """
        vertical_cells = {self[key] for key in vdw_map[vertical]["keys"]}
        horizontal_cells = {self[key] for key in vdw_map[horizontal]["keys"]}
        parity = vdw_map[vertical]["parity"] * vdw_map[horizontal]["parity"]
        diagonal_keys = vdw_key_map[parity]
        diagonal_major_index = vdw_index_map[parity]
        diagonal_minor_index = 1 if diagonal_major_index == 0 else 0
        diagonal_major = {self[key] for key in diagonal_keys[diagonal_major_index]}
        large_square = {self[4, 4]}.union(diagonal_major, vertical_cells, horizontal_cells)
        small_square = {self[key] for key in diagonal_keys[diagonal_minor_index]}
        return large_square, small_square

    def vdw_squares(self, vertical=None, horizontal=None) -> \
            list[tuple[set[Cell], set[Cell]]] | tuple[set[Cell], set[Cell]]:
        if min(isinstance(vertical, str), isinstance(horizontal, str)) is True:
            return self.single_vdw_square(vertical, horizontal)

        verticals = "top", "bottom" if vertical is None else [vertical]
        horizontals = "left", "right" if horizontal is None else [horizontal]

        squares = []
        for v, h in product([v for v in verticals], [h for h in horizontals]):
            squares.append(self.single_vdw_square(v, h))

        return squares
