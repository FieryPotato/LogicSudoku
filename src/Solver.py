import itertools
from collections import Iterable
from copy import deepcopy

from src.Cell import Cell
from src.Sudoku import Sudoku


class Solver:

    def __init__(self, sudoku: Sudoku):
        sudoku.update_pencil_marks()
        self.sudoku = sudoku
        self.is_solved = self.sudoku.is_complete
        self.easy_logic = (self.fill_naked_singles, self.fill_hidden_singles,
                           self.check_for_naked_tuples, self.check_for_locked_candidates,
                           self.check_for_pointing_tuple)
        self.intermediate_logic = tuple()
        self.levels = (self.try_easy_logic, self.try_intermediate_logic)

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

    def try_intermediate_logic(self) -> bool:
        for strategy in self.intermediate_logic:
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
            for group_type in "row", "column", "box":
                if self.check_digit_in_cell_for_group_hidden_single(digit, cell, group_type):
                    return True
        return False

    def check_for_naked_tuples(self) -> bool:
        operated = False
        for size in range(2, 5):
            for group_type in "rows", "columns", "boxes":
                for group in getattr(self.sudoku, group_type):
                    empty_cells = [cell for cell in group if cell.is_empty]
                    for test_tuple in itertools.combinations(empty_cells, r=size):
                        tuple_options = set()
                        for cell in test_tuple:
                            tuple_options = tuple_options.union(cell.pencil_marks)
                        if len(tuple_options) == size:
                            non_members: set = (set([cell.coordinates for cell in group])
                                                - set([cell.coordinates for cell in test_tuple]))
                            for coordinates in non_members:
                                cell = self.sudoku[coordinates]
                                if cell.pencil_marks.intersection(tuple_options):
                                    cell.pencil_marks -= set(tuple_options)
                                    operated = True
                            if operated:
                                return True
        return False

    def check_for_locked_candidates(self) -> bool:
        operated = False
        for digit in range(1, 10):
            for group_type in "rows", "columns":
                group_list: list[list[Cell]] = getattr(self.sudoku, group_type)
                for group in group_list:
                    possible_cells: list[Cell] = [cell for cell in group if digit in cell.pencil_marks]
                    if len(set([cell.box_num for cell in possible_cells])) == 1:
                        locked_box = set([cell.coordinates
                                          for cell in self.sudoku.box(possible_cells[0].box_num)])
                        for coordinates in locked_box - set(c.coordinates for c in possible_cells):
                            self.eliminate_locked_candidate_pencil_marks(coordinates, digit, group, group_type)
                            operated = True
        return operated

    def eliminate_locked_candidate_pencil_marks(self, coordinates, digit, group, group_type):
        cell = self.sudoku[coordinates]
        if digit in cell.pencil_marks:
            if group_type == "rows":
                if cell.y != group[0].y:
                    cell.pencil_marks.remove(digit)
            elif group_type == "columns":
                if cell.x != group[0].x:
                    cell.pencil_marks.remove(digit)

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

    def check_for_hidden_tuples(self) -> bool:
        operated = False
        for size in range(2, 5):
            for group_type in "rows", "columns", "boxes":
                for group in getattr(self.sudoku, group_type):
                    for possible_options in itertools.combinations(range(1, 10), r=size):
                        possible_cells = [cell for cell in group
                                          if options_in_cell_min(possible_options, cell)]
                        if len(possible_cells) == size:
                            if set(possible_options) <= overlapping_elements(
                                    *[cell.pencil_marks for cell in possible_cells]
                            ):
                                group_minus_possibles = [c for c in group if c not in possible_cells]
                                for cell in group_minus_possibles:
                                    if cell.pencil_marks.intersection(set(possible_options)):
                                        break
                                else:
                                    for cell in possible_cells:
                                        for option in tuple(cell.pencil_marks):
                                            if option not in possible_options:
                                                cell.pencil_marks.remove(option)
                                                operated = True
                        if operated:
                            return operated
        return False


def options_in_cell_min(options: Iterable, cell: Cell) -> bool:
    """Return true if any options are in cell.pencil_marks."""

    for option in options:
        if option in cell.pencil_marks:
            return True
    return False


def overlapping_elements(*args: set) -> set:
    """Return a set containing all elements shared by two or more of args."""

    all_digits = []
    for digit_set in args:
        all_digits.extend(digit for digit in digit_set)
    check_set = set()
    overlap = set()
    for digit in all_digits:
        if digit in check_set:
            overlap.add(digit,)
        check_set.add(digit,)
    return overlap

