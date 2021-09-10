import itertools
from typing import ItemsView, Union, KeysView, Iterator

from src.Cell import Cell


CELL_KEYS: list = [(j, i) for i, j in itertools.product(range(9), repeat=2)]
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
        if type(other) == self.__class__:
            if self.cell_dict == other.cell_dict:
                return True
        return False

    def __ne__(self, other) -> bool:
        if type(other) == self.__class__:
            if self.cell_dict == other.cell_dict:
                return False
        return True

    def __setitem__(self, key, value) -> None:
        self.cell_dict[key] = value
        return None

    def __getitem__(self, item) -> Cell:
        return self.cell_dict[item]

    def __delitem__(self, key) -> None:
        del self.cell_dict[key]
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
        row_digits: set = {self[c].digit for c in cell.row}
        column_digits: set = {self[c].digit for c in cell.column}
        box_digits: set = {self[c].digit for c in cell.box}
        invalid_digits: set = row_digits.union(column_digits, box_digits)
        cell.pencil_marks -= invalid_digits
        
    @classmethod
    def from_string(cls, string) -> "Sudoku":
        """Return a sudoku whose cells in order appear in an 81-character string."""
        if len(string) != 81:
            raise ValueError
        new = cls()
        for i, key in enumerate(CELL_KEYS):
            new[key].fill(string[i])
        return new

    def update_pencil_marks(self) -> None:
        """Update all pencil marks in the puzzle based only on cell/row/box
         logic."""
        for key in self.keys():
            self.check_cell_pencil_marks(key)

    def box(self, i) -> list[Cell]:
        """Return the list of cells in box i of the Sudoku."""
        return [self[cell] for cell in BOX_MAP[i]]
