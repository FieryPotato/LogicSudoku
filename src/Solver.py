RANGE_SET = {i for i in range(1, 10)}


class Solver:
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.tracker: tuple[int, int] = (-1, -1)

    def main(self):
        if not self.solve():
            print("No solution was found.")
        return self.sudoku

    def solve(self, col=0, row=0):
        """Solve the sudoku recursively and return the sudoku if there is a solution"""

        current_cell = col, row
        next_cell = col + 1, row
        if col == 9:  # If we are at the end of the row
            if row == 8:  # If we are at the last line of the puzzle
                return True
            else:
                current_cell = 0, row + 1
                next_cell = 1, row + 1
        if not self.sudoku[current_cell].is_empty:
            return self.solve(*next_cell)
        for digit in RANGE_SET:
            if self.sudoku.is_valid(current_cell, digit):
                self.sudoku.set_cell(current_cell, digit)
                if self.solve(*next_cell):
                    return True
            self.sudoku[current_cell].clear()
        return False
