import itertools
from collections.abc import Iterable
from copy import deepcopy
from typing import Optional, Generator, Union, Any

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

        self.basic_logic = self.fill_naked_singles, self.fill_hidden_singles
        self.easy_logic = self.check_for_naked_tuples, self.check_for_locked_candidates, self.check_for_pointing_tuple
        self.intermediate_logic = self.check_for_hidden_tuples, self.check_for_xwings
        self.hard_logic = self.check_for_ywings, self.check_for_avoidable_rectangles
        self.brutal_logic = self.check_for_xyzwings, self.check_for_unique_rectangles
        self.galaxy_brain_logic = ()

        self.levels = (self.try_basic_logic, self.try_easy_logic, self.try_intermediate_logic,
                       self.try_hard_logic, self.try_brutal_logic)

    def main(self):
        if not self.is_solved:
            backup = None
            while backup != self.sudoku:
                backup = deepcopy(self.sudoku)
                for level in self.levels:
                    if level():
                        break
            self.is_solved = self.sudoku.is_complete

    def try_basic_logic(self) -> bool:
        for strategy in self.basic_logic:
            if strategy():
                return True
        return False

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

    def try_hard_logic(self) -> bool:
        for strategy in self.hard_logic:
            if strategy():
                return True
        return False

    def try_brutal_logic(self) -> bool:
        for strategy in self.brutal_logic:
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
                                  _options_in_cell_min(possible_options, cell)]
                if len(possible_cells) == size:
                    if (set(possible_options) <= _overlapping_elements(
                            *[cell.pencil_marks for cell in possible_cells])):
                        if self.clear_hidden_tuple(group, possible_cells, possible_options):
                            return True
        return False

    def check_for_xwings(self) -> bool:
        size = 2

        for group_type, digit in itertools.product(RC, range(1, 10)):
            for indices in itertools.combinations(range(9), r=size):
                candidates: list[list[Cell]] = [self.cells_in_group_with_digit_in_pm(digit, index, group_type) for index
                                                in indices]

                if min([len(x) == len(y) == size for x, y in itertools.combinations(candidates, r=2)]):
                    candidate_cells = [cell for candidate in candidates for cell in candidate]  # candidates flattened
                    cross_groups = [group for group in zip(*candidates)]
                    check_group, check_param = _xwing_param_group_values(group_type)

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
        Return a list of cells in the group with input digit in its pencil marks.
        :param digit: a digit from 1 to 9
        :param group_index: a digit from 1 to 9
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
        triples = self.find_ywing_triples()
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

    def find_ywing_triples(self) -> list[tuple[Cell, Cell, Cell]]:
        """
        Return a list of tuples of cells in self.sudoku which meet
        the following criteria:

        - all cells have 2 options;
        - each cell hase 1 and only 1 overlapping option with each other cell;
        - the cells together have a total of 3 unique options between them.
        """

        return [
            (a, b, c) for a, b, c in itertools.combinations(self.sudoku, r=3)
            if ((len(a.pencil_marks) == len(b.pencil_marks) == len(c.pencil_marks) == 2)
                and (len(a.pencil_marks.intersection(b.pencil_marks)) ==
                     len(a.pencil_marks.intersection(c.pencil_marks)) ==
                     len(b.pencil_marks.intersection(c.pencil_marks)) == 1)
                and (len(a.pencil_marks.union(b.pencil_marks, c.pencil_marks)) == 3))
        ]

    def potential_avoidable_rectangles(self) -> Generator[tuple[Cell, Cell, Cell, Cell], None, None]:
        for quad in itertools.combinations(self.sudoku, r=4):
            top_left, top_right, bot_left, bot_right = quad
            # if cells are arranged in a rectangle
            if (top_left.y == top_right.y and bot_left.y == bot_right.y
                    and top_left.x == bot_left.x and top_right.x == bot_right.x
                    and top_left.x != bot_right.x and top_left.y != bot_right.y):

                if min([cell.started_empty for cell in quad]):
                    if len({cell.box_num for cell in quad}) == 2:
                        if len([cell for cell in quad if cell.is_empty]) == 1:
                            yield top_left, top_right, bot_left, bot_right

    def check_for_avoidable_rectangles(self) -> bool:
        for quad in self.potential_avoidable_rectangles():
            if self.clear_avoidable_rectangle(*quad):
                return True
        return False

    def check_for_xyzwings(self) -> bool:
        possibles = self.find_xyzwings()
        for possible in possibles:
            if self.clear_xyzwing(*possible):
                return True
        return False

    @staticmethod
    def clear_xyzwing(targets, digit):
        operated = False
        for cell in targets:
            if digit in (pencil_marks := cell.pencil_marks):
                pencil_marks.remove(digit)
                operated = True
        return operated

    def find_xyzwings(self) -> Union[tuple[list[Cell], int], Any]:
        """Return a pair of lists of cells a and b which satisfy the following:

        - there are three cells in b;
        - the size of two cells is b's pencil marks is 2, and the other 3
        - the size of the union of pencil marks in b cells is 3;
        - the size of the intersection of pencil marks in b cells is 1
        - the cell in b with 3 pencil marks sees both other cells in b
        - cells in a see all cells in b;
        - cells in a have the cell in b's pencil marks' intersection in their pencil marks

        If no such lists exist, return two empty tuples.
        """
        possible_xyzwings = []
        for index, triple in self.possible_xyzwing_triples():
            shared_digit = self.xyzwing_triple_shared_digit(index, triple)
            affected_cells = self.xyzwing_affected_cells(shared_digit, triple)
            possible_xyzwings.append([affected_cells, shared_digit])
        return possible_xyzwings

    def possible_xyzwing_triples(self) -> Generator[tuple[int, [Cell, Cell, Cell]], None, None]:
        for triple in itertools.combinations(self.sudoku, r=3):
            if len({cell.box_num for cell in triple}) != 2:
                continue

            indices = {0, 1, 2}
            for i in range(3):
                axis = triple[i]
                wings = [triple[x] for x in indices - {i}]
                if len(axis.pencil_marks) == 3 and len(wings[0].pencil_marks) == len(wings[1].pencil_marks) == 2:
                    yield i, triple

    def xyzwing_affected_cells(self, shared_digit, triple) -> list:
        affected_cells = []
        if affected_keys := set.intersection(*[cell.visible_cells() for cell in triple]):
            for key in affected_keys:
                cell = self.sudoku[key]
                if shared_digit in cell.pencil_marks:
                    affected_cells.append(cell)
        return affected_cells

    def check_for_unique_rectangles(self) -> bool:
        for box in self.sudoku.boxes:
            pairs = [cell for cell in box if len(cell.pencil_marks) == 2]
            for cell_a, cell_b in itertools.combinations(pairs, r=2):
                if cell_a.x != cell_b.x and cell_a.y != cell_b.y:
                    continue
                if cell_a.pencil_marks != cell_b.pencil_marks:
                    continue

                cell, target = self.unique_rectangle_cell_and_target(cell_a, cell_b)

                if cell is not None and target is not None:
                    if intersection := cell.pencil_marks.intersection(target.pencil_marks):
                        target.remove(intersection)
                        return True
        return False

    def unique_rectangle_cell_and_target(self, cell_a, cell_b):
        """Given cell_a, cell_b that share a row or column in the same box
        and have identical pencil_marks, return a cell (if any) that shares a
        column or row (respectively) with one of them and the cell that
        completes the rectangle."""
        cell, target = None, None
        # a and b share a row
        if cell_a.y == cell_b.y:
            for key in [k for k in cell_a.column if k != cell_a.coordinates]:
                cell = self.sudoku[key]
                if cell.pencil_marks == cell_a.pencil_marks:
                    target = self.sudoku[(cell_b.x, cell.y)]
                    break
            else:
                for key in [k for k in cell_b.column if k != cell_b.coordinates]:
                    cell = self.sudoku[key]
                    if cell.pencil_marks == cell_b.pencil_marks:
                        target = self.sudoku[(cell_a.x, cell.y)]
                        break
        # a and b share a column
        elif cell_a.x == cell_b.x:
            for key in [k for k in cell_a.row if k != cell_a.coordinates]:
                cell = self.sudoku[key]
                if cell.pencil_marks == cell_a.pencil_marks:
                    target = self.sudoku[(cell.x, cell_b.y)]
                    break
            else:
                for key in [k for k in cell_b.row if k != cell_b.coordinates]:
                    cell = self.sudoku[key]
                    if cell.pencil_marks == cell_a.pencil_marks:
                        target = self.sudoku[(cell.x, cell_a.y)]
                        break
        return cell, target

    def check_for_pointing_rectangles(self) -> bool:
        for a, b in itertools.combinations([cell for cell in self.sudoku if cell.is_empty], r=2):
            if not a.sees(b): continue
            if a.pencil_marks != b.pencil_marks: continue
            if a.y == b.y:
                for key in a.column:
                    c = self.sudoku[key]
                    d = self.sudoku[(b.x, c.y)]
                    digits = self._pointing_rectangle_digits(a, b, c, d)
                    if not digits: continue
                    if self.clear_pointing_rectangle((c, d), digits, "row"):
                        return True
            elif a.x == b.x:
                for key in a.row:
                    c = self.sudoku[key]
                    d = self.sudoku[(c.x, b.y)]
                    digits = self._pointing_rectangle_digits(a, b, c, d)
                    if not digits: continue
                    if self.clear_pointing_rectangle((c, d), digits, "column"):
                        return True
            else: continue
        return False

    def clear_pointing_rectangle(self, pointing_pair, extra_digits, group) -> bool:
        operated = False
        c, d = pointing_pair
        for pointing in [self.sudoku[key] for key in getattr(c, group)]:
            if pointing.pencil_marks == extra_digits:
                pointed_keys = Cell.intersection(c, d, pointing)
                pointed = [self.sudoku[key] for key in pointed_keys]
                for cell in pointed:
                    cell.remove(pointing.pencil_marks)
                    operated = True
        return operated

    @staticmethod
    def _pointing_rectangle_digits(a, b, c, d) -> set:
        if c.is_empty:
            if c.pencil_marks.issuperset(a.pencil_marks):
                if d.is_empty:
                    if d.pencil_marks.issuperset(b.pencil_marks):
                        return set.union(
                            *[c.pencil_marks - a.pencil_marks, d.pencil_marks - a.pencil_marks]
                        )

    @staticmethod
    def xyzwing_triple_shared_digit(index, triple: tuple[Cell, Cell, Cell]) -> Optional[int]:
        """Return triple's shared digit if input triple is a viable xyzwing;
        returns None otherwise."""
        axis = triple[index]
        wings = [triple[x] for x in {0, 1, 2} - {index}]
        if min([axis.sees(cell) for cell in wings]):
            pencil_marks = [cell.pencil_marks for cell in triple]
            intersection = set.intersection(*pencil_marks)
            if len(set.union(*pencil_marks)) == 3 and len(set.intersection(*pencil_marks)) == 1:
                return intersection.pop()
        return None

    @staticmethod
    def find_valid_ywings(triples) -> list[Optional[list[Cell, Cell]]]:
        """Return either an empty list or a list containing pairs of
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

    @staticmethod
    def clear_avoidable_rectangle(top_left, top_right, bot_left, bot_right) -> bool:
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


def _options_in_cell_min(options: Iterable, cell: Cell) -> bool:
    """Return true if any options are in cell.pencil_marks."""
    for option in options:
        if option in cell.pencil_marks:
            return True
    return False


def _overlapping_elements(*args: set) -> set:
    """Return a set containing all elements shared by two or more of args.
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


def _xwing_param_group_values(group_type) -> tuple[str, str]:
    check_param, check_group = None, None
    if group_type == "rows":
        check_param = "x"
        check_group = "column"
    elif group_type == "columns":
        check_param = "y"
        check_group = "row"
    return check_group, check_param
