class Solver:
    def __init__(self, sudoku):
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
