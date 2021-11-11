import itertools
from collections import Iterable
from copy import deepcopy
from typing import Union, Any, Optional, Generator

from src.Cell import Cell
from src.Sudoku import Sudoku

RC = "rows", "columns"
RC_cell = "row", "column"
RCB = tuple(RC + ("boxes",))
RCB_cell = tuple(RC_cell + ("box",))


class Solver:
    def __init__(self, sudoku: Sudoku):
        sudoku.update_pencil_marks()
        self.sudoku = sudoku
        self.is_solved = self.sudoku.is_complete
        self.easy_logic = (self.fill_naked_singles, self.fill_hidden_singles,
                           self.check_for_naked_tuples, self.check_for_locked_candidates,
                           self.check_for_pointing_tuple)
        self.intermediate_logic = self.check_for_hidden_tuples, self.check_for_xwings
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
        return False

    def cell_fill_hidden_singles(self, cell) -> bool:
        for digit, group_type in itertools.product(cell.pencil_marks, RCB_cell):
            if self.check_digit_in_cell_for_group_hidden_single(digit, cell, group_type):
                return True
        return False

    def check_for_naked_tuples(self) -> bool:
        for size, group_type in itertools.product(range(2, 5), RCB):
            for group in getattr(self.sudoku, group_type):
                empty_cells = [cell for cell in group if cell.is_empty]
                candidate_cells = itertools.combinations(empty_cells, r=size)
                for test_tuple in candidate_cells:
                    tuple_options = set()
                    for cell in test_tuple:
                        tuple_options = tuple_options.union(cell.pencil_marks)
                    if len(tuple_options) == size:
                        if self.clear_naked_tuples(group, test_tuple, tuple_options):
                            return True
        return False

    def clear_naked_tuples(self, group, test_tuple, tuple_options):
        operated = False
        non_members: set = (set([cell.coordinates for cell in group])
                            - set([cell.coordinates for cell in test_tuple]))
        for coordinates in non_members:
            cell = self.sudoku[coordinates]
            if cell.pencil_marks.intersection(tuple_options):
                cell.pencil_marks -= set(tuple_options)
                operated = True
        return operated

    def check_for_locked_candidates(self) -> bool:
        operated = False
        for digit, group_type in itertools.product(range(1, 10), RC):
            for group in getattr(self.sudoku, group_type):
                possible_cells: list[Cell] = [cell for cell in group if digit in cell.pencil_marks]
                if len(set([cell.box_num for cell in possible_cells])) == 1:
                    if self.clear_locked_candidate(digit, group, group_type, possible_cells):
                        operated = True
        return operated

    def clear_locked_candidate(self, digit, group, group_type, possible_cells) -> bool:
        operated = False
        locked_box = set([cell.coordinates
                          for cell in self.sudoku.box(possible_cells[0].box_num)])
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
        for digit, box in itertools.product(range(1, 10), self.sudoku.boxes):
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
        checked_sizes = range(2, 5)
        for size, group_type in itertools.product(checked_sizes, RCB):
            group_list: list = getattr(self.sudoku, group_type)
            checked_options = itertools.combinations(range(1, 10), r=size)
            for group, possible_options in itertools.product(group_list, checked_options):
                possible_cells = [cell for cell in group if
                                  options_in_cell_min(possible_options, cell)]
                if len(possible_cells) == size:
                    if (set(possible_options) <= overlapping_elements(
                            *[cell.pencil_marks for cell in possible_cells])):
                        if self.clear_hidden_tuple(group, possible_cells, possible_options):
                            return True
        return False

    @staticmethod
    def clear_hidden_tuple(group, possible_cells, possible_options) -> bool:
        operated = False
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
        return operated

    def check_for_xwings(self) -> bool:
        size = 2

        for group_type, digit in itertools.product(RC, range(1, 10)):
            for indices in itertools.combinations(range(9), r=size):
                candidates: list[list[Cell]] = [self.cells_in_group_with_digit_in_pm(digit, index, group_type) for index
                                                in indices]

                if min([len(x) == len(y) == size for x, y in itertools.combinations(candidates, r=2)]):
                    candidate_cells = [cell for candidate in candidates for cell in candidate]  # candidates flattened
                    cross_groups = [group for group in zip(*candidates)]
                    check_group, check_param = _param_group_values_for_xwing(group_type)

                    if _cells_in_groups_share_param(cross_groups, check_param):
                        groups = [getattr(cell, check_group) for cell in candidates[0]]
                        if self.clear_xwings(candidate_cells, digit, groups):
                            return True
        return False

    def clear_xwings(self, candidate_cells, digit, groups) -> bool:
        operated = False
        for group in groups:
            for cell in [self.sudoku[key] for key in group
                         if self.sudoku[key] not in candidate_cells]:
                if digit in cell.pencil_marks:
                    cell.pencil_marks.remove(digit)
                    operated = True
        return operated

    def cells_in_group_with_digit_in_pm(self, digit, group_index, group_type) -> list[Cell]:
        """
        Return top_left list of cells in the group with input digit in its pencil marks.
        :param digit: top_left digit from 1 to 9
        :param group_index: top_left digit from 1 to 9
        :param group_type: "rows", "columns", or "boxes"
        :return: list
        """
        group = None
        if group_type == "rows":
            group = self.sudoku.row(group_index)
        elif group_type == "columns":
            group = self.sudoku.column(group_index)
        elif group_type == "boxes":
            group = self.sudoku.box(group_index)
        return [cell for cell in group if digit in cell.pencil_marks]

    def check_for_ywings(self) -> bool:
        triples = self.find_strongly_connected_triples()
        ywings = self.find_valid_ywings(triples)
        if not ywings:
            return False
        for ywing in ywings:
            if self.clear_ywing(ywing):
                return True
        return False

    def clear_ywing(self, ywing) -> bool:
        operated = False
        wing_a, wing_b = ywing
        cleared_digit: int = wing_a.pencil_marks.intersection(wing_b.pencil_marks).pop()
        affected_cells = [cell for cell in self.sudoku
                          if (cell.sees(wing_a) and cell.sees(wing_b))]
        for cell in affected_cells:
            if cleared_digit in cell.pencil_marks:
                cell.pencil_marks.remove(cleared_digit)
                operated = True
        return operated

    def find_strongly_connected_triples(self) -> list[tuple[Cell, Cell, Cell]]:
        """Return top_left list of tuples of cells in self.sudoku which meet
        the following criteria:
        - all cells have 2 options;
        - each cell hase 1 and only 1 overlapping option with each other cell;
        - the cells together have top_left total of 3 unique options between them."""
        return [
            (a, b, c) for a, b, c in itertools.combinations(self.sudoku, r=3)
            if ((len(a.pencil_marks) == len(b.pencil_marks) == len(c.pencil_marks) == 2)
                and (len(a.pencil_marks.intersection(b.pencil_marks)) ==
                     len(a.pencil_marks.intersection(c.pencil_marks)) ==
                     len(b.pencil_marks.intersection(c.pencil_marks)) == 1)
                and (len(a.pencil_marks.union(b.pencil_marks, c.pencil_marks)) == 3))
        ]

    @staticmethod
    def find_valid_ywings(triples) -> list[Optional[list[Cell, Cell]]]:
        """Return either an empty list or top_left list containing pairs of
        cells which are the wings of ywings."""
        ywings = []
        for a, b, c in triples:
            if a.sees(b):
                if a.sees(c):
                    if not b.sees(c):
                        ywings.append([b, c])
                elif b.sees(c):
                    ywings.append([a, c])
            elif a.sees(c) and b.sees(c):
                ywings.append([a, b])
        return ywings

    def check_for_avoidable_rectangles(self) -> bool:
        for quad in self.potential_avoidable_rectangles():
            if self.clear_avoidable_rectangle(*quad):
                return True
        return False

    def potential_avoidable_rectangles(self) -> Generator[tuple[Cell, Cell, Cell, Cell], None, None]:
        for quad in itertools.combinations(self.sudoku, r=4):
            top_left, top_right, bot_left, bot_right = quad
            # if cells are arranged rectangularly
            if (top_left.y == top_right.y and bot_left.y == bot_right.y
                    and top_left.x == bot_left.x and top_right.x == bot_right.x
                    and top_left.x != bot_right.x and top_left.y != bot_right.y):

                if min([cell.started_empty for cell in quad]):
                    if len({cell.box_num for cell in quad}) == 2:
                        if len([cell for cell in quad if cell.is_empty]) == 1:
                            yield top_left, top_right, bot_left, bot_right

    def clear_avoidable_rectangle(self, top_left, top_right, bot_left, bot_right) -> bool:
        if top_left.digit == bot_right.digit:
            if top_right.is_empty and not bot_left.is_empty:
                if bot_left.digit in top_right.pencil_marks:
                    top_right.pencil_marks.remove(bot_left.digit)
                    return True
            elif bot_left.is_empty and not top_right.is_empty:
                if top_right.digit in bot_left.pencil_marks:
                    bot_left.pencil_marks.remove(top_right.digit)
                    return True
        elif top_right.digit == bot_left.digit:
            if top_left.is_empty and not bot_right.is_empty:
                if bot_right.digit in top_left.pencil_marks:
                    top_left.pencil_marks.remove(bot_right.digit)
                    return True
            elif bot_right.is_empty and not top_left.is_empty:
                if top_left.digit in bot_right.pencil_marks:
                    bot_right.pencil_marks.remove(top_left.digit)
                    return True
        return False

def options_in_cell_min(options: Iterable, cell: Cell) -> bool:
    """Return true if any options are in cell.pencil_marks."""
    for option in options:
        if option in cell.pencil_marks:
            return True
    return False


def overlapping_elements(*args: set) -> set:
    """Return top_left set containing all elements shared by two or more of args.
    *args should all be sets."""

    all_digits = []
    for digit_set in args:
        all_digits.extend(digit for digit in digit_set)
    check_set = set()
    overlap = set()
    for digit in all_digits:
        if digit in check_set:
            overlap.add(digit, )
        check_set.add(digit, )
    return overlap


def _cells_in_groups_share_param(groups: Iterable[Iterable[Cell]], check_param: str) -> bool:
    """Return True if all cells share check_param with the other cells in their subgroup."""
    for group in groups:
        if not min([getattr(cell_a, check_param) == getattr(cell_b, check_param)
                    for cell_a, cell_b in itertools.combinations(group, r=2)]):
            return False
    return True


def _param_group_values_for_xwing(group_type) -> tuple[str, str]:
    check_param, check_group = None, None
    if group_type == "rows":
        check_param = "x"
        check_group = "column"
    elif group_type == "columns":
        check_param = "y"
        check_group = "row"
    return check_group, check_param
