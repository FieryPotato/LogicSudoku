from collections.abc import Iterable
from copy import deepcopy
from itertools import combinations, product, permutations
from typing import Optional, Generator, Union, Any

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
        self.brutal_logic = (self.check_for_xyzwings, self.check_for_unique_rectangle,
                             self.check_for_pointing_rectangle, self.check_for_hidden_rectangle)
        self.galaxy_brain_logic = (self.check_for_skyscraper,)

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
            for digit, group_type in product(cell.pencil_marks, RCB):
                axis = LITERALS[group_type]["check_axis"]
                group = getattr(self.sudoku, group_type)(getattr(cell, axis))
                if self.only_one_cell_in_group_can_contain_digit(digit, group):
                    cell.fill(digit)
                    self.sudoku.update_pencil_marks()
                    return True
        return False

    def check_for_naked_tuple(self) -> bool:
        for size, group_type in product(range(2, 5), RCB_ITER):
            for group in getattr(self.sudoku, group_type):
                empty_cells = [cell for cell in group if cell.is_empty]
                candidate_tuples = combinations(empty_cells, r=size)
                for candidate_tuple in candidate_tuples:
                    if self.cells_form_naked_tuple(*candidate_tuple):
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
        for group_type, digit in product(RC_ITER, range(1, 10)):
            for group in getattr(self.sudoku, group_type):
                cells_with_digit = {cell
                                    for cell in group
                                    if digit in cell}
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

    def check_for_skyscraper(self) -> bool:
        for digit in range(1, 10):
            for group_type in RC:
                iter_group = LITERALS[group_type]["iter_group"]
                groups = getattr(self.sudoku, iter_group)
                for group_pair in combinations(groups, r=2):
                    trimmed = [{cell for cell in group_pair[n] if digit in cell} for n in range(2)]
                    if not min([len(g) == 2 for g in trimmed]): continue
                    if self.clear_skyscraper(digit, trimmed, group_type):
                        return True
        return False

    def clear_skyscraper(self, digit, group_pair, group_type) -> bool:
        for pair in product(*group_pair):
            if self.cells_share_opposite_group(group_type, *pair):
                skyscraper = set(pair)
                seers = (set(group_pair[0]).union(set(group_pair[1]))) - set(skyscraper)
                cells = {self.sudoku[key] for key in Cell.intersection(*seers)}
                if self.remove_digits_from_cells(digit, *cells):
                    return True
        return False

    def cells_share_same_group(self, group_type, *cells) -> bool:
        if group_type == "row":
            return self.cells_share_a_row(*cells)
        elif group_type == "column":
            return self.cells_share_a_column(*cells)
        else:
            raise ValueError(f"{group_type} is not a valid argument for"
                             f" Solver.cells_share_same_group.")

    def cells_share_opposite_group(self, group_type, *cells) -> bool:
        if group_type == "row":
            return self.cells_share_a_column(*cells)
        elif group_type == "column":
            return self.cells_share_a_row(*cells)
        else:
            raise ValueError(f"{group_type} is not a valid argument for"
                             f"Solver.cells_share_opposite_group.")

    @staticmethod
    def remove_digits_from_cells(digits: Union[int, Iterable[int]], *cells: Cell) -> bool:
        operated = False
        for cell in cells:
            if cell.remove(digits):
                operated = True
        return operated

    def check_for_pointing_tuple(self) -> bool:
        for digit, box in product(range(1, 10), self.sudoku.boxes):
            pointing = {cell for cell in box if digit in cell}
            pointed = self._cells_seen_by_pointing_tuple(pointing)
            if self.remove_digits_from_cells(digit, *pointed):
                return True
        return False

    @staticmethod
    def cells_share_a_row(*cells: Iterable[Cell]) -> bool:
        return len({cell.y for cell in cells}) == 1

    @staticmethod
    def cells_share_a_column(*cells: Iterable[Cell]) -> bool:
        return len({cell.x for cell in cells}) == 1

    @staticmethod
    def cells_share_a_box(*cells: Iterable[Cell]) -> bool:
        """Return whether input cells share a box."""
        return len({cell.box_num for cell in cells}) == 1

    @staticmethod
    def cells_form_a_rectangle(*cells: Iterable[Cell]) -> bool:
        """Return whether input cells form a rectangle."""
        if len(cells) != 4: return False
        for order in permutations(cells, r=4):
            a, b, c, d = order
            if a.x == c.x and a.y == b.y and d.x == b.x and d.y == c.y:
                return True
        return False

    @staticmethod
    def only_one_cell_in_group_can_contain_digit(digit, group) -> bool:
        return len({cell for cell in group if digit in cell}) == 1

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
        sizes = range(2, 5)
        for size, group_type in product(sizes, RCB):
            iter_group = LITERALS[group_type]["iter_group"]
            groups = getattr(self.sudoku, iter_group)
            for group in groups:
                if self.clear_hidden_tuple(group, size):
                    return True
        return False

    def clear_hidden_tuple(self, group, size) -> bool:
        for digits in combinations(range(1, 10), r=size):
            candidate_tuple = self.cells_in_group_with_digits(digits, group)
            if len(candidate_tuple) != size: continue
            if self.cells_form_hidden_tuple(digits, candidate_tuple):
                other_digits = set(range(1, 10)) - set(digits)
                if self.remove_digits_from_cells(other_digits, *candidate_tuple):
                    return True
        return False

    @staticmethod
    def cells_form_hidden_tuple(digits, candidate_tuple) -> bool:
        digits = set(digits)
        cells_individually_contain_at_least_two_of_digits = min(
            [len(cell.pencil_marks.intersection(digits)) >= 2
             for cell in candidate_tuple]
        )
        cells_together_contain_all_digits = digits.issubset(
            set.union(*[cell.pencil_marks for cell in candidate_tuple])
        )
        return cells_individually_contain_at_least_two_of_digits and cells_together_contain_all_digits

    @staticmethod
    def cells_in_group_with_digits(digits, group):
        empty_cells = {cell for cell in group if cell.is_empty}
        cells_with_digits = [
            {cell for cell in empty_cells if digit in cell} for digit in digits
        ]
        flattened_cells = {cell for _list in cells_with_digits for cell in _list}
        return flattened_cells

    def check_for_fish(self) -> bool:
        """Fish include X-wings, Swordfish, and Jellyfish."""
        sizes = 2, 3, 4
        for size, group_type, digit in product(sizes, RC, range(1, 10)):
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

        for perp_group in perpendicular_fish_groups:
            group_index = (getattr(next(iter(perp_group)), opposite_axis))
            group = getattr(self.sudoku, opposite_group)(group_index)
            cells = [cell for cell in group if cell not in perp_group]
            if self.remove_digits_from_cells(digit, *cells):
                operated = True
        return operated

    @staticmethod
    def perpendicular_groups(group_list: list[list[Cell]], group_type: str) -> list[list[Cell]]:
        """Converts lists of cells grouped by row or column into lists
        of those same cells grouped by column or row, respectively."""
        opposite_axis = LITERALS[group_type]["opposite_axis"]
        perpendicular_groups = []
        all_cells = [cell for group in group_list for cell in group]
        axes = {getattr(cell, opposite_axis) for cell in all_cells}
        for axis in axes:
            perpendicular_groups.append([cell for cell in all_cells if getattr(cell, opposite_axis) == axis])
        return perpendicular_groups

    @staticmethod
    def trimmed_fish_groups(candidate_groups, group_type, size) -> Optional[tuple]:
        """Return group of cells that could be an xwing, swordfish, or jellyfish."""
        opposite_axis = LITERALS[group_type]["opposite_axis"]
        for candidates in combinations(candidate_groups, r=size):
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
            candidate_cells = [cell for cell in group if digit in cell]
            if 2 <= len(candidate_cells) <= size:
                candidate_groups.append(candidate_cells)
        return candidate_groups

    def check_for_ywing(self) -> bool:
        triples = self.find_ywing_triples()
        if ywings := self.find_valid_ywings(triples):
            for ywing in ywings:
                if self.clear_ywing(ywing):
                    return True
        return False

    def clear_ywing(self, ywing) -> bool:
        operated = False
        wing_a, wing_b = ywing
        shared_digit: int = wing_a.pencil_marks.intersection(wing_b.pencil_marks).pop()
        affected_cells = {cell for cell in self.sudoku
                          if (cell.sees(wing_a) and cell.sees(wing_b))}
        if self.remove_digits_from_cells(shared_digit, *affected_cells):
            return True
        return operated

    def find_ywing_triples(self) -> list[tuple[Cell, Cell, Cell]]:
        """
        Return a list of tuples of cells in self.sudoku which meet
        the following criteria:

        - there are three cells in the tuple
        - all cells have 2 options;
        - each cell hase 1 and only 1 overlapping option with each other cell;
        - the cells together have a total of 3 unique options between them.
        """

        return [
            (a, b, c) for a, b, c in combinations(self.sudoku, r=3)
            if ((len(a.pencil_marks) == len(b.pencil_marks) == len(c.pencil_marks) == 2)
                and (len(a.pencil_marks.intersection(b.pencil_marks))
                     == len(a.pencil_marks.intersection(c.pencil_marks))
                     == len(b.pencil_marks.intersection(c.pencil_marks))
                     == 1)
                and (len(a.pencil_marks.union(b.pencil_marks, c.pencil_marks)) == 3))
        ]

    def potential_avoidable_rectangles(self) -> Generator[tuple[Cell, Cell, Cell, Cell], None, None]:
        """Yield only groups of cells that form a rectangle and which
        could break uniqueness."""
        for rectangle in self.sudoku.rectangles():
            if self.rectangle_is_avoidable(rectangle):
                yield rectangle

    @staticmethod
    def rectangle_is_avoidable(rectangle) -> bool:
        """Return true if filling in the rectangle improperly would
         break uniqueness."""
        if (min([cell.started_empty for cell in rectangle])
                and len({cell.box_num for cell in rectangle}) == 2
                and len([cell for cell in rectangle if cell.is_empty]) == 1):
            return True

    def check_for_avoidable_rectangle(self) -> bool:
        for rectangle in self.potential_avoidable_rectangles():
            if self.clear_avoidable_rectangle(*rectangle):
                return True
        return False

    def check_for_xyzwings(self) -> bool:
        for index, triple in self.possible_xyzwing_triples():
            if self.clear_xyzwing(index, triple):
                return True
        return False

    def clear_xyzwing(self, index, triple):
        shared_digit = self.xyzwing_triple_shared_digit(index, triple)
        affected_cells = self.xyzwing_affected_cells(shared_digit, triple)
        if self.remove_digits_from_cells(shared_digit, *affected_cells):
            return True
        return False

    def possible_xyzwing_triples(self) -> Generator[tuple[int, [Cell, Cell, Cell]], None, None]:
        for triple in combinations(self.sudoku, r=3):
            if len({cell.box_num for cell in triple}) != 2:
                continue

            indices = set(range(3))
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
                if shared_digit in cell:
                    affected_cells.append(cell)
        return affected_cells

    def check_for_unique_rectangle(self) -> bool:
        for box in self.sudoku.boxes:
            pairs = [cell for cell in box if len(cell.pencil_marks) == 2]
            for a, b in combinations(pairs, r=2):
                if self.cells_form_naked_tuple(a, b):
                    cell, target = self.unique_rectangle_cell_and_target(a, b)

                    if cell is not None and target is not None:
                        if intersection := cell.pencil_marks.intersection(target.pencil_marks):
                            target.remove(intersection)
                            return True
        return False

    def unique_rectangle_cell_and_target(self, a, b):
        """Given cell_a, cell_b that share a row or column in the same box
        and have identical pencil_marks, return a cell (if any) that shares a
        column or row (respectively) with one of them and the cell that
        completes the rectangle."""
        cell, target = None, None
        # a and b share a row
        if a.y == b.y:
            for cell in [self.sudoku[k] for k in a.column if k != a.coordinates]:
                if cell.pencil_marks == a.pencil_marks:
                    target = self.sudoku[(b.x, cell.y)]
                    break
            else:
                for cell in [self.sudoku[k] for k in b.column if k != b.coordinates]:
                    if cell.pencil_marks == b.pencil_marks:
                        target = self.sudoku[(a.x, cell.y)]
                        break
        # a and b share a column
        elif a.x == b.x:
            for cell in [self.sudoku[k] for k in a.row if k != a.coordinates]:
                if cell.pencil_marks == a.pencil_marks:
                    target = self.sudoku[(cell.x, b.y)]
                    break
            else:
                for cell in [self.sudoku[k] for k in b.row if k != b.coordinates]:
                    if cell.pencil_marks == a.pencil_marks:
                        target = self.sudoku[(cell.x, a.y)]
                        break
        return cell, target

    def check_for_pointing_rectangle(self) -> bool:
        for a, b in combinations([cell for cell in self.sudoku if cell.is_empty], r=2):
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
        operated = False
        if top_left.digit == bot_right.digit:
            if top_right.is_empty and not bot_left.is_empty:
                if bot_left.digit in top_right.pencil_marks:
                    top_right.pencil_marks.remove(bot_left.digit)
                    operated = True
            elif bot_left.is_empty and not top_right.is_empty:
                if top_right.digit in bot_left.pencil_marks:
                    bot_left.pencil_marks.remove(top_right.digit)
                    operated = True
        elif top_right.digit == bot_left.digit:
            if top_left.is_empty and not bot_right.is_empty:
                if bot_right.digit in top_left.pencil_marks:
                    top_left.pencil_marks.remove(bot_right.digit)
                    operated = True
            elif bot_right.is_empty and not top_left.is_empty:
                if top_left.digit in bot_right.pencil_marks:
                    bot_right.pencil_marks.remove(top_left.digit)
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

    @staticmethod
    def _at_least_one_cell_has_only_two_options(*cells) -> bool:
        return bool([cell
                     for cell in cells
                     if len(cell.pencil_marks) == 2])

    @staticmethod
    def cells_are_empty(*cells) -> bool:
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
            if not self.cells_are_strongly_connected_by_digit(digit, *group):
                break
        else:
            digit_to_remove = focus.pencil_marks - {digit}
            if opposite.remove(digit_to_remove):
                return True
        return False

    def _check_for_hidden_rectangle_pairs(self, rectangle) -> bool:
        for group_type, pair in product(RC, combinations(rectangle, r=2)):
            check_axis = LITERALS[group_type]["check_axis"]

            if self.cells_share_axis(check_axis, *pair) and self.cells_form_naked_tuple(*pair):
                pencil_marks = pair[0].pencil_marks
                opposite_pair: set[Cell, Cell] = {*rectangle} - {*pair}
                if self.all_cells_in_group_contain_pencil_marks(opposite_pair, pencil_marks) is False:
                    continue
                for digit in pencil_marks:
                    if self.cells_are_strongly_connected_by_digit(digit, *opposite_pair):
                        if self._clear_hidden_rectangle_pair(digit, opposite_pair, pencil_marks):
                            return True

    @staticmethod
    def cells_form_naked_tuple(*cells) -> bool:
        """Return whether input cells cumulatively contain exactly as
        many possible digits as there are input cells."""
        pencil_marks = [cell.pencil_marks for cell in cells]
        flattened_pms = {digit for group in pencil_marks for digit in group}
        if len(set.union(flattened_pms)) != len(cells):
            return False
        return True

    @staticmethod
    def cells_share_axis(check_axis, *cells: Cell) -> bool:
        """Return whether input cells all share a row or column.
        check_axes should be 'x' for column or 'y' for row."""
        axes = {getattr(cell, check_axis) for cell in cells}
        return len(axes) == 1

    @staticmethod
    def all_cells_in_group_contain_pencil_marks(group: Iterable[Cell], pencil_marks: set[int]) -> bool:
        """Return whether all cells in cells contain each digit in pencil_marks."""
        return min([
            cell.pencil_marks.issuperset(pencil_marks)
            for cell in group
        ])

    def cells_are_strongly_connected_by_digit(self, digit: int, *cells: Cell) -> bool:
        """Return whether input cells are the only two cells in their
        row, or column that can be digit."""
        if self.cells_share_a_column(*cells):
            axis = "x"
            group_type = "column"
        elif self.cells_share_a_row(*cells):
            axis = "y"
            group_type = "row"
        elif self.cells_share_a_box(*cells):
            axis = "box_num"
            group_type = "box"
        else:
            return False
        return len([
            cell
            for cell in getattr(self.sudoku, group_type)(getattr([*cells][0], axis))
            if digit in cell
        ]) == 2

    @staticmethod
    def _clear_hidden_rectangle_pair(digit, pair, pencil_marks):
        operated = False
        removed_digit = next(iter(d for d in pencil_marks if d != digit))
        for focus in pair:
            if focus.remove(removed_digit):
                operated = True
        return operated

    def find_strongly_connected_pairs_with_digit(self, digit: int) -> set[tuple[Cell, Cell]]:
        pairs = []
        for group_type in RCB_ITER:
            for group in getattr(self.sudoku, group_type):
                cells_with_digit = {cell for cell in group if digit in cell}
                if len(cells_with_digit) == 2:
                    pairs.append(tuple(cells_with_digit))
        return set(pairs)

    def strongly_connected_cell_chains(self, pairs: set[tuple[Cell, Cell]]):
        """Return a list of lists of cells which form a chain of three or
        more cells that are strongly connected."""
        adjacencies: dict = self.strongly_connected_chain_adjacent_cells(pairs)
        endpoints = {k for k, v in adjacencies.items() if len(v) == 1}
        return self.match_endpoints_with_adjacencies(adjacencies, endpoints)

    def match_endpoints_with_adjacencies(self, adjacencies, endpoints):
        """Match each endpoint cell with adjacent cells and return the
        results after pruning duplicates."""
        chains = [[cell] for cell in endpoints]
        no_change_counter = 0
        while (
                max([chain[0] == chain[-1] or chain[-1] not in endpoints
                     for chain in chains])
        ):
            no_change_counter = 0
            for chain in chains:
                cell: Cell = chain[-1]
                connected: set[Cell] = {c for c in adjacencies[cell]}
                for checked in chain:
                    connected -= {checked}
                if len(connected) == 0:
                    no_change_counter += 1
                    continue
                elif len(connected) == 1:
                    chain.append(next(iter(connected)))
                else:
                    chains.remove(chain)
                    for other_cell in connected:
                        new_chain = [_cell for _cell in chain]
                        new_chain.append(other_cell)
                        chains.append(new_chain)
            if no_change_counter == len(chains):
                break
        self.remove_duplicate_chains(chains)
        return chains

    def remove_duplicate_chains(self, chains: list[list[Cell]]) -> None:
        """Remove colour_chains from the input that are either too short or
        duplicates (but reversed)."""
        chain_pairs = ((x, y) for x, y in combinations(chains, r=2) if len(x) == len(y))
        for x, y in chain_pairs:
            if x in chains and len(x) <= 2:
                chains.remove(x)
            if y in chains and x == y[::-1]:
                chains.remove(y)

    def strongly_connected_chain_adjacent_cells(self, pairs) -> dict[Cell, set[Cell]]:
        """Return a dictionary mapping each cell appearing in pairs to each
        cell it shares a pair with."""
        flat_cells = {cell for pair in pairs for cell in pair}
        chain_dict = {
            cell: set()
            for cell in flat_cells
        }
        for k in chain_dict:
            pairs_with_k = [set(pair) for pair in pairs if k in pair]
            for pair in pairs_with_k:
                chain_dict[k].update(pair - {k})
        return chain_dict

    def colour_pairs_for_strongly_connected_chains(self, chains) -> list[list[list[Cell]]]:
        result = []
        for chain in chains:
            evens = []
            odds = []
            for i, cell in enumerate(chain):
                if i % 2 == 0:
                    evens.append(cell)
                elif i % 2 == 1:
                    odds.append(cell)
            result.append([evens, odds])
        return result

    def cells_seen_by_colour_chains(self, colour_chains: list[list[list[Cell]]]) -> set[Union[Cell, Any]]:
        result = set()
        for chain_pair in colour_chains:
            for seer_pair in product(*chain_pair):
                seen = {self.sudoku[key] for key in Cell.intersection(*seer_pair)}
                result.update({cell for cell in seen if cell.is_empty})
        return result

    def check_for_2_string_kite(self) -> bool:
        for digit in range(1, 10):
            strongly_connected_pairs = self.find_strongly_connected_pairs_with_digit(digit)
            if not strongly_connected_pairs: continue
            strongly_connected_chains = self.strongly_connected_cell_chains(strongly_connected_pairs)
            coloured_chains = self.colour_pairs_for_strongly_connected_chains(strongly_connected_chains)
            seen_cells = self.cells_seen_by_colour_chains(coloured_chains)
            if self.remove_digits_from_cells(digit, *seen_cells):
                return True
        return False

    def check_for_finned_xwings(self) -> bool:
        for digit, group_type in product(range(1, 10), RC):
            iter_group = LITERALS[group_type]["iter_group"]
            for group_pair in combinations(getattr(self.sudoku, iter_group), r=2):
                if (finned_x_wing_groups := self.finned_x_wing_groups(digit, *group_pair)) is None:
                    continue

                x_wing_group, fin_group = finned_x_wing_groups
                if (affected_cells := self.finned_x_wing_affected_cells(group_type, x_wing_group, fin_group)) is None:
                    continue
                if self.remove_digits_from_cells(digit, *affected_cells):
                    return True
        return False

    def finned_x_wing_groups(self, digit, a: list[Cell], b: list[Cell]) -> Optional[tuple[list[Cell], list[Cell]]]:
        """Return two line groups if they might contain a finned x-wing. Otherwise return two empty lists"""
        x_wing_group = []
        fin_group = []
        for group in a, b:
            if len([cell for cell in group if digit in cell]) == 2:
                x_wing_group = group
            elif len([cell for cell in group if digit in cell]) in {3, 4}:
                fin_group = group
            else:
                break
        x_wing_group: list[Cell] = [cell for cell in x_wing_group if digit in cell]
        fin_group: list[Cell] = [cell for cell in fin_group if digit in cell]
        if x_wing_group and fin_group:
            return x_wing_group, fin_group
        return None

    def x_wing_if_it_has_fins(self, group_type, fin_group, x_wing_group) -> list:
        """Return the x-wing hidden inside a finned x-wing if such an x-wing exists."""
        opposite_axis = LITERALS[group_type]["opposite_axis"]
        for fin_0, fin_1 in combinations(fin_group, r=2):
            checktangle = [
                x_wing_group[0],
                fin_0,
                x_wing_group[1],
                fin_1
            ]
            if self.cells_form_a_rectangle(*checktangle):
                return checktangle
        return []

    def finned_x_wing_affected_cells(self, group_type, x_wing_group, fin_group) -> Optional[set[Cell]]:
        if not (finned_x_wing := self.x_wing_if_it_has_fins(group_type, fin_group, x_wing_group)):
            return None
        fins: set[Cell] = set(fin_group) - set(finned_x_wing)
        for cell in set(fin_group) - set(fins):
            if self.cells_share_a_box(cell, *fins):
                affected_finned_cell: Cell = cell
                break
        else:
            return None

        opposite_group = LITERALS[group_type]["opposite_group"]
        opposite_axis = LITERALS[group_type]["opposite_axis"]

        affected_box: list[Cell] = getattr(self.sudoku, "box")(affected_finned_cell.box_num)
        affected_axis: int = getattr(affected_finned_cell, opposite_axis)
        affected_non_box_group: list[Cell] = getattr(self.sudoku, opposite_group)(affected_axis)
        affected_cells = {cell for cell in affected_box if cell in affected_non_box_group}
        affected_cells -= set(fin_group).union(set(x_wing_group))

        return affected_cells
