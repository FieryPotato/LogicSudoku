from itertools import product, permutations, combinations
from typing import ItemsView, Union, KeysView, Iterator, Generator, overload

from src.Cell import Cell

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

    def is_legal(self, return_cell=False) -> Union[bool, tuple[int, int]]:
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

    def get_cell(self, coordinates) -> Union[int, str]:
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

    @classmethod
    def from_string(cls, string, edited=None) -> "Sudoku":
        """Return a sudoku whose cells in order appear in an 81-character string."""
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

    def rectangles(self) -> Generator[tuple[Cell, Cell, Cell, Cell], None, None]:
        """Yield cells arranged in a rectangle."""
        for row in self.rows:
            for top_left, top_right in combinations(row, r=2):
                for bottom_left in [self[key]
                                    for key in top_left.visible_cells("column")
                                    if key[1] > top_left.y]:
                    bottom_right = self[top_right.x, bottom_left.y]
                    yield top_left, top_right, bottom_left, bottom_right

    def house_contains_filled_digit(self, digit: int, house: list[Cell]) -> bool:
        """Return whether input house of self contains input digit."""
        house_digits = {cell.digit for cell in house if not cell.is_empty}
        return digit in house_digits

    def houses_with_digit(self, house_type: str, digit: int) -> Generator[list[Cell], None, None]:
        iter_house_type = house_type + "s"
        for house in getattr(self, iter_house_type):
            if len([cell for cell in house if digit in cell]):
                yield house
