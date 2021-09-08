from src.Sudoku import Sudoku


GROUPS: tuple = ("row", "column", "box")


class Solver:
    def __init__(self, sudoku: Sudoku):
        sudoku.update_pencil_marks()
        self.sudoku = sudoku

    def main(self):
        while not self.sudoku.is_complete:
            self.fill_naked_singles()
            self.fill_hidden_singles()

    def fill_naked_singles(self) -> None:
        backup = None
        while backup != self.sudoku:
            backup = self.sudoku
            self.sudoku.update_pencil_marks()
            for key, cell in self.sudoku.items():
                if len(cell.pencil_marks) == 1:
                    cell.fill(*cell.pencil_marks)
        return None

    def fill_hidden_singles(self) -> None:
        backup = None
        while backup != self.sudoku:
            backup = self.sudoku
            self.sudoku.update_pencil_marks()
            for key, cell in self.sudoku.items():
                self.cell_fill_hidden_singles(cell)

    def cell_fill_hidden_singles(self, cell) -> None:
        for digit in cell.pencil_marks:
            for group in GROUPS:
                self.check_digit_in_cell_for_group_hidden_single(digit, cell, group)

    def check_digit_in_cell_for_group_hidden_single(self, digit, cell, group) -> None:
        pencil_marks = [self.sudoku[c].pencil_marks for c in getattr(cell, group)]
        pencil_marks.remove(cell.pencil_marks)
        for valid_set in pencil_marks:
            if digit in valid_set:
                break
        else:
            cell.fill(digit)

    def check_for_naked_pairs(self) -> None:
        backup = None
        while backup != self.sudoku:
            backup = self.sudoku
            self.sudoku.update_pencil_marks()
            # self.check_box_for_naked_pairs()

    def check_box_for_naked_pairs(self) -> None:
        for key, cell in self.sudoku.items():
            if len(cell.pencil_marks) == 2:
                # group_minus_cell =
                pass

