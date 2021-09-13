from typing import Optional

from src.Cell import Cell
from src.Sudoku import Sudoku


class Solver:
    def __init__(self, sudoku: Sudoku):
        sudoku.update_pencil_marks()
        self.sudoku = sudoku

    def main(self):
        while not self.sudoku.is_complete:
            self.fill_naked_singles()
            self.fill_hidden_singles()
            self.check_for_naked_pairs()

    def fill_naked_singles(self) -> None:
        backup: Optional[Sudoku] = None
        while backup != self.sudoku:
            backup = self.sudoku
            for key, cell in self.sudoku.items():
                if len(cell.pencil_marks) == 1:
                    cell.fill(*cell.pencil_marks)
            self.sudoku.update_pencil_marks()
        return None

    def fill_hidden_singles(self) -> None:
        backup: Optional[Sudoku] = None
        while backup != self.sudoku:
            backup = self.sudoku
            for key, cell in self.sudoku.items():
                self.cell_fill_hidden_singles(cell)
            self.sudoku.update_pencil_marks()

    def cell_fill_hidden_singles(self, cell) -> None:
        for digit in cell.pencil_marks:
            for group in "row", "column", "box":
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
        backup: Optional[Sudoku] = None
        while backup != self.sudoku:
            backup = self.sudoku
            for cell in self.sudoku:
                groups = "row", "box", "column"
                for group in groups:
                    self.check_cell_in_group_for_naked_pairs(cell, group)

    def check_cell_in_group_for_naked_pairs(self, cell, group_type) -> None:
        if len(cell.pencil_marks) == 2:
            group: list[Cell] = [self.sudoku[c] for c in getattr(cell, group_type)]
            group.remove(cell)
            for c in group:
                if c.pencil_marks == cell.pencil_marks:
                    group.remove(c)
                    clear_pencil_marks_from_naked_single_group(group, cell)

    def check_for_locked_candidates(self) -> None:
        for digit in range(1, 10):
            for group in "rows", "columns":
                self.check_digit_for_locked_candidates_in_group(digit, group)

    def check_digit_for_locked_candidates_in_group(self, digit, group) -> None:
        for g in getattr(self.sudoku, group):
            candidate_cells: list[Cell] = [cell for cell in g if digit in cell.pencil_marks]
            if len(candidate_cells) <= 3:
                box_numbers = [cell.box_num for cell in candidate_cells]
                if len(set(box_numbers)) == 1:
                    self.clear_pencil_marks_from_locked_candidate_cells(candidate_cells, digit)

    def clear_pencil_marks_from_locked_candidate_cells(self, cells, digit) -> None:
        box_number = cells[0].box_num
        locked_box = self.sudoku.box(box_number)
        locked_cells = [cell for cell in locked_box if cell not in cells]
        for remainder in locked_cells:
            if digit in remainder.pencil_marks:
                remainder.pencil_marks.remove(digit)

    def check_for_pointing_tuple(self) -> None:
        for digit in range(1, 10):
            for box in self.sudoku.boxes:
                possibles = [cell for cell in box if digit in cell.pencil_marks]
                rows = set(c.y for c in possibles)
                columns = set(c.x for c in possibles)

                if len(rows) == 1:
                    pointed_group = self.sudoku.row(list(rows)[0])
                    for cell in pointed_group:
                        if cell not in possibles and digit in cell.pencil_marks:
                            cell.pencil_marks.remove(digit)

                elif len(columns) == 1:
                    pointed_group = self.sudoku.column(list(columns)[0])
                    for cell in pointed_group:
                        if cell not in possibles and digit in cell.pencil_marks:
                            cell.pencil_marks.remove(digit)





def clear_pencil_marks_from_naked_single_group(group, cell):
    for remainder in group:
        for digit in cell.pencil_marks:
            if digit in remainder.pencil_marks:
                remainder.pencil_marks.remove(digit)
