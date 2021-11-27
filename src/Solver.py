import itertools
from collections.abc import Iterable
from copy import deepcopy
from typing import Optional, Generator, Union, Any, List, Tuple

from src.Cell import Cell
from src.Sudoku import Sudoku

RC_ITER = "rows", "columns"
RC = "row", "column"
RCB_ITER = tuple(RC_ITER + ("boxes",))
RCB = tuple(RC + ("box",))

LITERALS = {
    "row": {
        "iter_group": "rows",
        "single_group": "row",
        "check_axis": "y",
        "opposite_iter_group": "columns",
        "opposite_group": "column",
        "opposite_axis": "x",
    },
    "column": {
        "iter_group": "columns",
        "single_group": "column",
        "check_axis": "x",
        "opposite_iter_group": "rows",
        "opposite_group": "row",
        "opposite_axis": "y"
    },
    "box": {
        "iter_group": "boxes",
        "single_group": "box",
        "check_axis": "box_num",
        "opposite_iter_group": None,
        "opposite_group": None,
        "opposite_axis": None
    }
}


class Solver:
    def __init__(self, sudoku: Sudoku):
        sudoku.update_pencil_marks()
        self.sudoku = sudoku
        self.is_solved = self.sudoku.is_complete

        self.basic_logic = self.fill_naked_singles, self.fill_hidden_singles
        self.easy_logic = (self.check_for_naked_tuple, self.check_for_locked_candidate,
                           self.check_for_pointing_tuple)
        self.intermediate_logic = self.check_for_hidden_tuple, self.check_for_fish
        self.hard_logic = self.check_for_ywing, self.check_for_avoidable_rectangle
        self.brutal_logic = (self.check_for_xyzwing, self.check_for_unique_rectangle,
                             self.check_for_pointing_rectangle, self.check_for_hidden_rectangle)
        self.galaxy_brain_logic = ()

        self.levels = (self.try_basic_logic, self.try_easy_logic, self.try_intermediate_logic,
                       self.try_hard_logic, self.try_brutal_logic)

    def main(self) -> bool:
        if not self.is_solved:
            backup = None
            while backup != self.sudoku:
                backup = deepcopy(self.sudoku)
                for level in self.levels:
                    if level():
                        break
            self.is_solved = self.sudoku.is_complete
        return self.is_solved

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
        for cell in self.sudoku:
            if len(cell.pencil_marks) == 1:
                cell.fill(*cell.pencil_marks)
                self.sudoku.update_pencil_marks()
                return True
        return False

    def fill_hidden_singles(self) -> bool:
        for cell in self.sudoku:
            for digit, group_type in itertools.product(cell.pencil_marks, RCB):
                axis = LITERALS[group_type]["check_axis"]
                group = getattr(self.sudoku, group_type)(getattr(cell, axis))
                if self._only_one_cell_in_group_can_contain_digit(digit, group):
                    cell.fill(digit)
                    self.sudoku.update_pencil_marks()
                    return True
        return False

    def _only_one_cell_in_group_can_contain_digit(self, digit, group) -> bool:
        return len({cell for cell in group if digit in cell.pencil_marks}) == 1

    def check_for_naked_tuple(self) -> bool:
        for size, group_type in itertools.product(range(2, 5), RCB_ITER):
            for group in getattr(self.sudoku, group_type):
                empty_cells = [cell for cell in group if cell.is_empty]
                candidate_tuples = itertools.combinations(empty_cells, r=size)
                for candidate_tuple in candidate_tuples:
                    if self.cells_form_a_tuple(*candidate_tuple):
                        if self.clear_naked_tuples(group, candidate_tuple):
                            return True
        return False

    def clear_naked_tuples(self, group, tuple_cells):
        non_members: set[Cell] = set(group) - set(tuple_cells)
        marks = [tuple(cell.pencil_marks) for cell in tuple_cells]
        options = {digit for pms in marks for digit in pms}
        if self.remove_digits_from_cells(options, *non_members):
            return True

    def check_for_locked_candidate(self) -> bool:
        for group_type, digit in itertools.product(RC_ITER, range(1, 10)):
            for group in getattr(self.sudoku, group_type):
                cells_with_digit = {cell
                                    for cell in group
                                    if digit in cell.pencil_marks}
                if self.cells_share_a_box(*cells_with_digit):
                    if self.clear_locked_candidate(cells_with_digit, digit):
                        return True
        return False

    def clear_locked_candidate(self, locked_candidate, digit) -> bool:
        box_num = next(iter(locked_candidate)).box_num
        affected = set(self.sudoku.box(box_num)) - locked_candidate
        if self.remove_digits_from_cells(digit, *affected):
            return True
        return False

    def cells_share_a_row(self, *cells: Cell) -> bool:
        return len({cell.y for cell in cells}) == 1

    def cells_share_a_column(self, *cells: Cell) -> bool:
        return len({cell.x for cell in cells}) == 1

    def cells_share_a_box(self, *cells: Cell) -> bool:
        return len({cell.box_num for cell in cells}) == 1

    def remove_digits_from_cells(self, digits: Union[int, Iterable[int]], *cells: Cell) -> bool:
        operated = False
        for cell in cells:
            if cell.remove(digits):
                operated = True
        return operated

    def check_for_pointing_tuple(self) -> bool:
        for digit, box in itertools.product(range(1, 10), self.sudoku.boxes):
            pointing = {cell for cell in box if digit in cell.pencil_marks}
            pointed = self._cells_seen_by_pointing_tuple(pointing)
            if self.remove_digits_from_cells(digit, *pointed):
                return True
        return False

    def _cells_seen_by_pointing_tuple(self, pointing):
        if self.cells_share_a_row(*pointing):
            pointed = set(self.sudoku.row(next(iter(pointing)).y))
        elif self.cells_share_a_column(*pointing):
            pointed = set(self.sudoku.column(next(iter(pointing)).x))
        else:
            return set()
        pointed -= pointing
        return pointed

    def check_for_hidden_tuple(self) -> bool:
        checked_sizes = range(2, 5)
        for size, group_type in itertools.product(checked_sizes, RCB_ITER):
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

    def check_for_fish(self) -> bool:
        """Fish include X-wings, Swordfish, and Jellyfish."""
        sizes = 2, 3, 4
        for size, group_type, digit in itertools.product(sizes, RC, range(1, 10)):
            candidate_groups = self.fish_candidate_groups(digit, group_type, size)
            fish_groups = self.trimmed_fish_groups(candidate_groups, group_type, size)
            if not fish_groups: continue
            if self.clear_fish(digit, fish_groups, group_type):
                return True
        return False

    def clear_fish(self, digit, fish_groups, group_type) -> bool:
        operated = False
        opposite_axis = LITERALS[group_type]["opposite_axis"]
        opposite_group = LITERALS[group_type]["opposite_group"]

        perpendicular_fish_groups = self.perpendicular_groups(fish_groups, group_type)

        for fish in perpendicular_fish_groups:
            for cell in [c for c in getattr(
                    self.sudoku, opposite_group
            )(
                getattr(fish[0], opposite_axis)
            ) if c not in fish
                         ]:
                if cell.remove(digit):
                    operated = True
        return operated

    def perpendicular_groups(self, group_list: list[list[Cell]], group_type: str) -> list[list[Cell]]:
        """Converts lists of cells grouped by row or column into lists
        of those same cells grouped by column or row, respectively."""
        opposite_axis = LITERALS[group_type]["opposite_axis"]
        perpendicular_groups = []
        all_cells = [cell for group in group_list for cell in group]
        axes = {getattr(cell, opposite_axis) for cell in all_cells}
        for axis in axes:
            perpendicular_groups.append([cell for cell in all_cells if getattr(cell, opposite_axis) == axis])
        return perpendicular_groups

    def trimmed_fish_groups(self, candidate_groups, group_type, size) -> Optional[tuple]:
        opposite_axis = LITERALS[group_type]["opposite_axis"]
        for candidates in itertools.combinations(candidate_groups, r=size):
            total_axes = set()
            for line in candidates:
                total_axes.update([getattr(cell, opposite_axis) for cell in line])
            if len(total_axes) == size:
                return candidates
        return None

    def fish_candidate_groups(self, digit, group_type, size) -> list[list[Cell]]:
        iter_group = LITERALS[group_type]["iter_group"]
        candidate_groups = []
        for group in getattr(self.sudoku, iter_group):
            candidate_cells = [cell for cell in group if digit in cell.pencil_marks]
            if 2 <= len(candidate_cells) <= size:
                candidate_groups.append(candidate_cells)
        return candidate_groups

    def cells_in_group_with_digit_in_pm(self, digit, group_index, group_type) -> list[Cell]:
        """
        Return a list of cells in the cells with input digit in its pencil marks.
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

    def check_for_ywing(self) -> bool:
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

    def check_for_avoidable_rectangle(self) -> bool:
        for quad in self.potential_avoidable_rectangles():
            if self.clear_avoidable_rectangle(*quad):
                return True
        return False

    def check_for_xyzwing(self) -> bool:
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

    def check_for_unique_rectangle(self) -> bool:
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

    def check_for_pointing_rectangle(self) -> bool:
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
            else:
                continue
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
    def _pointing_rectangle_digits(a: Cell, b: Cell, c: Cell, d: Cell) -> set:
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

    def check_for_hidden_rectangle(self) -> bool:
        for rectangle in self.sudoku.rectangles():
            if self.cells_are_empty(*rectangle) and self._at_least_one_cell_has_only_two_options(*rectangle):
                if self._check_for_hidden_rectangle_pairs(rectangle):
                    return True
                elif self._check_for_hidden_rectangle_singles(rectangle):
                    return True
        return False

    def _at_least_one_cell_has_only_two_options(self, *cells) -> bool:
        return bool([cell
                     for cell in cells
                     if len(cell.pencil_marks) == 2])

    def cells_are_empty(self, *cells) -> bool:
        """Return whether each cell in cells is empty."""
        return min([cell.is_empty for cell in cells])

    def _check_for_hidden_rectangle_singles(self, rectangle):
        for check_cell in rectangle:
            pencil_marks = check_cell.pencil_marks
            if len(pencil_marks) == 2:
                group = {*rectangle} - {check_cell}
                if self.all_cells_in_group_contain_pencil_marks(group, pencil_marks):
                    opposite = {opp
                                for opp in rectangle
                                if opp.x != check_cell.x and opp.y != check_cell.y}.pop()
                    for digit in pencil_marks:
                        if self.clear_single_hidden_rectangle(digit, check_cell, opposite):
                            return True
        return False

    def clear_single_hidden_rectangle(self, digit, focus, opposite) -> bool:
        for group_type in RC:
            check_axis = LITERALS[group_type]["check_axis"]
            single_group = LITERALS[group_type]["single_group"]

            group = getattr(self.sudoku, single_group)(getattr(opposite, check_axis))
            if not self.cells_are_closely_related_by_digit(digit, *group):
                break
        else:
            digit_to_remove = focus.pencil_marks - {digit}
            if opposite.remove(digit_to_remove):
                return True
        return False

    def _check_for_hidden_rectangle_pairs(self, rectangle) -> bool:
        for group_type, pair in itertools.product(RC, itertools.combinations(rectangle, r=2)):
            check_axis = LITERALS[group_type]["check_axis"]

            if self.cells_share_axis(check_axis, *pair) and self.cells_form_a_tuple(*pair):
                pencil_marks = pair[0].pencil_marks
                opposite_pair: set[Cell, Cell] = {*rectangle} - {*pair}
                if self.all_cells_in_group_contain_pencil_marks(opposite_pair, pencil_marks) is False:
                    continue
                for digit in pencil_marks:
                    if self.cells_are_closely_related_by_digit(digit, *opposite_pair):
                        if self._clear_hidden_rectangle_pair(digit, opposite_pair, pencil_marks):
                            return True

    def cells_form_a_tuple(self, *cells) -> bool:
        """Return whether input cells cumulatively contain exactly as
        many possible digits as there are input cells."""
        pencil_marks = [cell.pencil_marks for cell in cells]
        flattened_pms = {digit for group in pencil_marks for digit in group}
        if len(set.union(flattened_pms)) != len(cells):
            return False
        return True

    def cells_share_axis(self, check_axis, *cells: Cell) -> bool:
        """Return whether input cells all share a row or column.
        check_axes should be 'x' for column or 'y' for row."""
        axes = {getattr(cell, check_axis) for cell in cells}
        return len(axes) == 1

    def all_cells_in_group_contain_pencil_marks(self, group: Iterable[Cell], pencil_marks: set[int]) -> bool:
        """Return whether all cells in cells contain each digit in pencil_marks."""
        return min([
            cell.pencil_marks.issuperset(pencil_marks)
            for cell in group
        ])

    def cells_are_closely_related_by_digit(self, digit: int, *cells: Cell) -> bool:
        """Return whether input cells are the only two cells in their
        row, or column that can be digit."""
        if len({cell.x for cell in cells}) == 1:
            axis = "x"
            group_type = "column"
        elif len({cell.y for cell in cells}) == 1:
            axis = "y"
            group_type = "row"
        else:
            return False
        return len([
            cell
            for cell in getattr(self.sudoku, group_type)(getattr([*cells][0], axis))
            if digit in cell.pencil_marks
        ]) == 2

    def _clear_hidden_rectangle_pair(self, digit, pair, pencil_marks):
        removed_digit = [d for d in pencil_marks if d != digit][0]
        for focus in pair:
            if focus.remove(removed_digit):
                operated = True
        return operated


def _options_in_cell_min(options: Iterable, cell: Cell) -> bool:
    """Return true if any options are in cell.pencil_marks."""
    for option in options:
        if option in cell.pencil_marks:
            return True
    return False


def _overlapping_elements(*args: set) -> set:
    """Return a set containing all elements shared by two or more of cells.
    *cells should all be sets."""

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
