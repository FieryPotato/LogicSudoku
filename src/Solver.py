import itertools
from typing import Optional
from copy import deepcopy

from src.Cell import Cell
from src.Sudoku import Sudoku


class Solver:

    def __init__(self, sudoku: Sudoku):
        sudoku.update_pencil_marks()
        self.sudoku = sudoku
        self.is_solved = self.sudoku.is_complete
        self.easy_logic = (self.fill_naked_singles, self.fill_hidden_singles,
                           self.check_for_naked_pairs, self.check_for_locked_candidates,
                           self.check_for_pointing_tuple)
        # "lambda: True" is only here to make self.levels a tuple of
        # callables until I write self.try_intermediate_logic
        self.levels = (self.try_easy_logic, lambda: True)

    def main(self):
        if not self.is_solved:
            backup = None
            while backup != self.sudoku:
                backup = deepcopy(self.sudoku)
                for level in self.levels:
                    level()
                    if backup != self.sudoku:
                        break
            self.is_solved = self.sudoku.is_complete

    def try_easy_logic(self) -> bool:
        backup: Optional[Sudoku] = None
        while backup != self.sudoku:
            backup = deepcopy(self.sudoku)
            for strategy in self.easy_logic:
                strategy()
                if backup != self.sudoku:
                    break
        return self.sudoku.is_complete

    def fill_naked_singles(self) -> None:
        backup: Optional[Sudoku] = None
        while backup != self.sudoku:
            backup = deepcopy(self.sudoku)
            for key, cell in self.sudoku.items():
                if len(cell.pencil_marks) == 1:
                    cell.fill(*cell.pencil_marks)
            self.sudoku.update_pencil_marks()
        return None

    def fill_hidden_singles(self) -> None:
        backup: Optional[Sudoku] = None
        while backup != self.sudoku:
            backup = deepcopy(self.sudoku)
            for key, cell in self.sudoku.items():
                self.cell_fill_hidden_singles(cell)
            self.sudoku.update_pencil_marks()
        return None

    def cell_fill_hidden_singles(self, cell) -> None:
        for digit in cell.pencil_marks:
            for group in "row", "column", "box":
                self.check_digit_in_cell_for_group_hidden_single(digit, cell, group)
        return None

    def check_for_naked_pairs(self) -> None:
        backup: Optional[Sudoku] = None
        while backup != self.sudoku:
            backup = deepcopy(self.sudoku)
            for cell in self.sudoku:
                groups = "row", "box", "column"
                for group in groups:
                    self.check_cell_in_group_for_naked_pairs(cell, group)
        return None

    def check_for_locked_candidates(self) -> None:
        for digit in range(1, 10):
            for group in "rows", "columns":
                self.check_digit_for_locked_candidates_in_group(digit, group)
        return None

    def check_for_pointing_tuple(self) -> None:
        for digit in range(1, 10):
            for box in self.sudoku.boxes:
                possibles = [cell for cell in box if digit in cell.pencil_marks]
                rows = set(c.y for c in possibles)
                cols = set(c.x for c in possibles)
                if len(rows) == 1:
                    pointed_group = self.sudoku.row(rows.pop())
                elif len(cols) == 1:
                    pointed_group = self.sudoku.column(cols.pop())
                else:
                    continue
                for cell in pointed_group:
                    if cell not in possibles and digit in cell.pencil_marks:
                        cell.pencil_marks.remove(digit)
        return None

    def check_digit_in_cell_for_group_hidden_single(self, digit, cell, group) -> None:
        pencil_marks = [self.sudoku[c].pencil_marks for c in getattr(cell, group)]
        pencil_marks.remove(cell.pencil_marks)
        for valid_set in pencil_marks:
            if digit in valid_set:
                break
        else:
            cell.fill(digit)
        return None

    def check_cell_in_group_for_naked_pairs(self, cell, group_type) -> None:
        if len(cell.pencil_marks) == 2:
            group: list[Cell] = [self.sudoku[c] for c in getattr(cell, group_type)]
            group.remove(cell)
            for c in group:
                if c.pencil_marks == cell.pencil_marks:
                    group.remove(c)
                    _clear_pencil_marks_from_naked_single_group(group, cell)
        return None

    def check_digit_for_locked_candidates_in_group(self, digit, group) -> None:
        for g in getattr(self.sudoku, group):
            candidate_cells: list[Cell] = [cell for cell in g if digit in cell.pencil_marks]
            if len(candidate_cells) <= 3:
                box_numbers = [cell.box_num for cell in candidate_cells]
                if len(set(box_numbers)) == 1:
                    self.clear_pencil_marks_from_locked_candidate_cells(candidate_cells, digit)
        return None

    def clear_pencil_marks_from_locked_candidate_cells(self, cells, digit) -> None:
        box_number = cells[0].box_num
        locked_box = self.sudoku.box(box_number)
        locked_cells = [cell for cell in locked_box if cell not in cells]
        for remainder in locked_cells:
            if digit in remainder.pencil_marks:
                remainder.pencil_marks.remove(digit)
        return None

    def check_for_hidden_pairs(self) -> None:
        backup: Optional[Sudoku] = None
        while backup != self.sudoku:
            backup = deepcopy(self.sudoku)
            groups = "row", "column", "box"
            for group_type in groups:
                for index in range(9):
                    self.check_group_for_hidden_pairs(group_type, index)
        return None

    def check_group_for_hidden_pairs(self, group_type: str, index: int) -> None:
        group: list[Cell]
        if group_type == "row":
            group = self.sudoku.row(index)
        elif group_type == "column":
            group = self.sudoku.column(index)
        elif group_type == "box":
            group = self.sudoku.box(index)
        for possible_a, possible_b in itertools.combinations(range(1, 10), 2):
            possible_cells = [cell for cell in group
                              if possible_a in cell.pencil_marks and possible_b in cell.pencil_marks]
            if len(possible_cells) == 2:
                for cell in [c for c in group if c not in possible_cells]:
                    if cell.pencil_marks.intersection({possible_a, possible_b}):
                        break
                else:
                    for cell in possible_cells:
                        cell.pencil_marks = {possible_a, possible_b}
                    break
        return None


def _clear_pencil_marks_from_naked_single_group(group, cell) -> None:
    for remainder in group:
        for digit in cell.pencil_marks:
            if digit in remainder.pencil_marks:
                remainder.pencil_marks.remove(digit)
    return None
