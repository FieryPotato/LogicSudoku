import itertools
from typing import Generator, ItemsView, Union, KeysView

from src.Cell import Cell


CELL_KEYS: list = [(j, i) for i, j in itertools.product(range(9), repeat=2)]


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

    def __iter__(self) -> Generator:
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
        cell: Cell = self[coordinates]
        row_digits: set = {self[c].digit for c in cell.row}
        column_digits: set = {self[c].digit for c in cell.column}
        box_digits: set = {self[c].digit for c in cell.box}
        invalid_digits: set = row_digits.union(column_digits, box_digits)
        cell.pencil_marks -= invalid_digits
        
    @classmethod
    def from_string(cls, string) -> "Sudoku":
        if len(string) != 81:
            raise ValueError
        new = cls()
        for i, key in enumerate(CELL_KEYS):
            new[key].fill(string[i])
        return new

    def update_pencil_marks(self):
        for key in self.keys():
            self.check_cell_pencil_marks(key)

    def box(self, i):
        pass
