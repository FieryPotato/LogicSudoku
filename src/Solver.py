from src.Cell import Cell
from src.Sudoku import Sudoku


GROUPS: tuple = ("row", "column", "box")


class Solver:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku
        for key in sudoku.keys():
            self.sudoku.check_cell_pencil_marks(key)

    def main(self):
        while not self.sudoku.is_complete:
            self.fill_naked_singles()

    def fill_naked_singles(self) -> None:
        backup = None
        while backup != self.sudoku:
            backup = self.sudoku
            for key, cell in self.sudoku.items():
                self.sudoku.check_cell_pencil_marks(key)
                if len(cell.pencil_marks) == 1:
                    cell.fill(*cell.pencil_marks)
        return None

    def fill_hidden_singles(self) -> None:
        backup = None
        while backup != self.sudoku:
            backup = self.sudoku
            for key, cell in self.sudoku.items():
                self.sudoku.check_cell_pencil_marks(key)
                self.cell_fill_hidden_singles(cell)

    def cell_fill_hidden_singles(self, cell) -> None:
        for digit in cell.pencil_marks:
            for group in GROUPS:
                self.check_digit_in_cell_for_group_hidden_single(digit, cell, group)

    def check_digit_in_cell_for_group_hidden_single(self, digit, cell, group):
        pencil_marks = [self.sudoku[c].pencil_marks for c in getattr(cell, group)]
        pencil_marks.remove(cell.pencil_marks)
        for valid_set in pencil_marks:
            if digit in valid_set:
                break
        else:
            cell.fill(digit)
