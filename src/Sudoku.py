import itertools

from Cell import Cell


CELL_KEYS = [(j, i) for i, j in itertools.product(range(9), repeat=2)]
RANGE_SET = {i for i in range(1, 10)}


class Sudoku:
    def __init__(self):
        self.cell_dict = {k: Cell(k) for k in CELL_KEYS}

    def __str__(self):
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

    def __eq__(self, other):
        if self.cell_dict == other.cell_dict:
            return True
        return False

    def __ne__(self, other):
        if self.cell_dict == other.cell_dict:
            return False
        return True

    def __setitem__(self, key, value):
        self.cell_dict[key] = value

    def __getitem__(self, item):
        return self.cell_dict[item]

    def __delitem__(self, key):
        del self.cell_dict[key]

    def items(self):
        return self.cell_dict.items()

    def set_cell(self, coordinates, value):
        self[coordinates].fill(value)
    
    def get_cell(self, coordinates):
        return self[coordinates].digit
        
    def is_valid(self, coordinates, digit):
        row_digits = {self[cell].digit for cell in self[coordinates].row}
        column_digits = {self[cell].digit for cell in self[coordinates].column}
        box_digits = {self[cell].digit for cell in self[coordinates].box}
        for group in (row_digits, column_digits, box_digits):
            if digit in group:
                return False
        return True
        
    @classmethod
    def from_string(cls, string):
        new = cls()
        for i, key in enumerate(CELL_KEYS):
            new[key].fill(string[i])
        return new
