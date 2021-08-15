from src.Sudoku import Sudoku


class Solver:
    def __init__(self, sudoku: Sudoku):
        self.sudoku = sudoku

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
            row_pencil_marks = [self.sudoku[c].pencil_marks for c in cell.row]
            row_pencil_marks.remove(cell.pencil_marks)

            for valid_set in row_pencil_marks:  # Indent these lines and put them under the for loop
                if digit in valid_set:          #
                    break                       #
            else:                               #
                cell.fill(digit)                #
