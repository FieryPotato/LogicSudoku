from src.Cell import Cell
from src.Sudoku import Sudoku


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
            self.check_digit_in_cell_for_row_hidden_single(cell, digit)
            self.check_digit_in_cell_for_col_hidden_single(cell, digit)

    def check_digit_in_cell_for_row_hidden_single(self, cell: Cell, digit: int) -> None:
        row_pencil_marks = [self.sudoku[c].pencil_marks for c in cell.row]
        row_pencil_marks.remove(cell.pencil_marks)
        for valid_set in row_pencil_marks:
            if digit in valid_set:
                break
        else:
            cell.fill(digit)

    def check_digit_in_cell_for_col_hidden_single(self, cell: Cell, digit: int) -> None:
        col_pencil_marks = [self.sudoku[c].pencil_marks for c in cell.column]
        col_pencil_marks.remove(cell.pencil_marks)
        for valid_set in col_pencil_marks:
            if digit in valid_set:
                break
        else:
            cell.fill(digit)
