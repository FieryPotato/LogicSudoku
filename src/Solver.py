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
                    if level():
                        break
            self.is_solved = self.sudoku.is_complete

    def try_easy_logic(self) -> bool:
        for strategy in self.easy_logic:
            if strategy():
                return True
        return False

    def fill_naked_singles(self) -> bool:
        for key, cell in self.sudoku.items():
            if len(cell.pencil_marks) == 1:
                cell.fill(*cell.pencil_marks)
                self.sudoku.update_pencil_marks()
                return True
        return False

    def fill_hidden_singles(self) -> bool:
        for key, cell in self.sudoku.items():
            if self.cell_fill_hidden_singles(cell):
                self.sudoku.update_pencil_marks()
                return True

    def cell_fill_hidden_singles(self, cell) -> bool:
        for digit in cell.pencil_marks:
            for group in "row", "column", "box":
                if self.check_digit_in_cell_for_group_hidden_single(digit, cell, group):
                    return True
        return False

    def check_for_naked_pairs(self) -> bool:
        for cell in self.sudoku:
            groups = "row", "box", "column"
            for group in groups:
                if self.check_cell_in_group_for_naked_pairs(cell, group):
                    return True
        return False

    def check_for_locked_candidates(self) -> bool:
        operated = False
        for digit in range(1, 10):
            for group_type in "rows", "columns":
                group_list = getattr(self.sudoku, group_type)
                for group in group_list:
                    possible_cells: list[Cell] = [cell for cell in group if digit in cell.pencil_marks]
                    if len(set([cell.box_num for cell in possible_cells])) == 1:
                        locked_box = set([cell.coordinates for cell in self.sudoku.box(possible_cells[0].box_num)])
                        for coordinates in locked_box - set(c.coordinates for c in possible_cells):
                            cell = self.sudoku[coordinates]
                            if digit in cell.pencil_marks:
                                if group_type == "rows":
                                    if cell.y != group[0].y:
                                        cell.pencil_marks.remove(digit)
                                elif group_type == "columns":
                                    if cell.x != group[0].x:
                                        cell.pencil_marks.remove(digit)
                                operated = True
        return operated

    def check_for_pointing_tuple(self) -> bool:
        operated = False
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
                        operated = True
        return operated

    def check_digit_in_cell_for_group_hidden_single(self, digit, cell, group) -> bool:
        pencil_marks = [self.sudoku[c].pencil_marks for c in getattr(cell, group)]
        pencil_marks.remove(cell.pencil_marks)
        for valid_set in pencil_marks:
            if digit in valid_set:
                break
        else:
            cell.fill(digit)
            return True
        return False

    def check_cell_in_group_for_naked_pairs(self, cell, group_type) -> bool:
        operated = False
        if len(cell.pencil_marks) == 2:
            group: list[Cell] = [self.sudoku[c] for c in getattr(cell, group_type)]
            group.remove(cell)
            for c in group:
                if c.pencil_marks == cell.pencil_marks:
                    group.remove(c)
                    self.clear_pencil_marks_from_naked_pair_group(group, cell)
                    operated = True
        return operated

    def check_for_hidden_pairs(self) -> bool:
        for index in range(9):
            groups = self.sudoku.row(index), self.sudoku.column(index), self.sudoku.box(index)
            for group in groups:
                if self.check_group_for_hidden_pairs(group):
                    return True
        return False

    def check_group_for_hidden_pairs(self, group: list[Cell]) -> bool:
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
                    return True
        return False

    def clear_pencil_marks_from_naked_pair_group(self, group, cell) -> None:
        for remainder in group:
            for digit in cell.pencil_marks:
                if digit in remainder.pencil_marks:
                    remainder.pencil_marks.remove(digit)
        return None
