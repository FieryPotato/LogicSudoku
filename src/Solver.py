from collections.abc import Iterable
from copy import deepcopy, copy
from itertools import combinations, product
from typing import Optional, Generator, Union, Any

from src.Cell import Cell
from src.Sudoku import Sudoku

RC_ITER = "rows", "columns"
RC = "row", "column"
RCB_ITER = tuple(RC_ITER + ("boxes",))
RCB = tuple(RC + ("box",))

LITERALS = {
    "row": {
        "iter_house": "rows",
        "single_house": "row",
        "check_axis": "y",
        "opposite_iter_house": "columns",
        "opposite_house": "column",
        "opposite_axis": "x",
    },
    "column": {
        "iter_house": "columns",
        "single_house": "column",
        "check_axis": "x",
        "opposite_iter_house": "rows",
        "opposite_house": "row",
        "opposite_axis": "y"
    },
    "box": {
        "iter_house": "boxes",
        "single_house": "box",
        "check_axis": "box_num",
        "opposite_iter_house": None,
        "opposite_house": None,
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
        self.galaxy_brain_logic = (self.check_for_skyscraper, self.check_for_two_colour_logic,
                                   self.check_for_empty_rectangle)

        self.levels = (self.try_basic_logic, self.try_easy_logic, self.try_intermediate_logic,
                       self.try_hard_logic, self.try_brutal_logic, self.try_galaxy_logic)

    # Super-methods

    def main(self) -> bool:
        """
        Solve as much of self.sudoku as possible and return whether it
        was successful.
        """
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

    def try_galaxy_logic(self) -> bool:
        for strategy in self.galaxy_brain_logic:
            if strategy():
                return True
        return False

    # Main Solver Logic Methods

    def fill_naked_singles(self) -> bool:
        """
        Fill cells that only have one pencil mark.
        """
        for cell in self.sudoku:
            if len(cell.pencil_marks) == 1:
                cell.fill(*cell.pencil_marks)
                self.sudoku.update_pencil_marks()
                return True
        return False

    def fill_hidden_singles(self) -> bool:
        """
        Fill cells that contain a unique pencil mark in a house.
        """
        for cell in self.sudoku:
            for digit, house_type in product(cell.pencil_marks, RCB):
                axis = LITERALS[house_type]["check_axis"]
                house = getattr(self.sudoku, house_type)(getattr(cell, axis))
                if len({cell for cell in house if digit in cell}) == 1:
                    cell.fill(digit)
                    self.sudoku.update_pencil_marks()
                    return True
        return False

    def check_for_avoidable_rectangle(self) -> bool:
        """
        Rectangles of cells that started empty and have 3 digits filled
        cannot contain identical digits across both diagonals.
        """
        for rectangle in self.potential_avoidable_rectangles():
            if self.clear_avoidable_rectangle(*rectangle):
                return True
        return False

    def check_for_empty_rectangle(self) -> bool:
        """
        If the cells in a house that cannot be a digit form a
        rectangle, then the cells that can be the digit are all on one
        row and one column. Any cell along one of those houses which
        sees a second cell that forms a strongly connected pair with a
        cell that lies on the other house cannot contain that digit,
        lest that house be unable to contain it at all.
        """
        for box in self.sudoku.boxes:
            unfilled_digits = {i for i in range(1, 10)} - {cell.digit for cell in box if not cell.is_empty}
            for digit in unfilled_digits:
                cells_without_digit = {cell for cell in box if digit not in cell}
                if len(cells_without_digit) < 4: continue
                for quadruple in combinations(cells_without_digit, r=4):
                    if Sudoku.cells_form_a_rectangle(*quadruple):
                        relevant_row_num = self.find_empty_rectangle_house("row", quadruple)
                        relevant_col_num = self.find_empty_rectangle_house("column", quadruple)
                        target_cell = self.find_empty_rectangle_perp_sc_cell(relevant_row_num, relevant_col_num, digit)
                        if target_cell is None: continue
                        if self.remove_digits_from_cells(digit, target_cell):
                            return True
        return False

    def check_for_fish(self) -> bool:
        """
        If n rows contain n cells with a digit and those cells lie on
        the same n columns, then other cells in those columns can't
        contain that digit. Likewise in the opposite direction. This
        includes x-wings, swordfish, and jellyfish.

        If one and only one of those rows contains more than n cells
        with the digit and those cells all share a box with one of the
        cells that shares a column as above, then other cells in that
        column not in that row but that are in the box can't contain
        that digit. This includes finned x-wings, finned swordfish, and
        finned jellyfish.
        :return:
        """
        sizes = [2, 3, 4]
        for size, digit, house_type in product(sizes, range(1, 10), RC):
            fish_candidate_groups = combinations(self.sudoku.houses_with_digit(house_type, digit), r=size)
            for fish_house_group in fish_candidate_groups:
                candidates = [[cell for cell in house if digit in cell] for house in fish_house_group]
                if min([2 <= len(candidate) <= size + 2 for candidate in candidates]):
                    check_axis = LITERALS[house_type]["check_axis"]
                    opposite_axis = LITERALS[house_type]["opposite_axis"]
                    if len({getattr(cell, check_axis) for house in candidates for cell in house}) \
                            == len({getattr(cell, opposite_axis) for house in candidates for cell in house}):
                        if self.solve_proper_fish(digit, house_type, candidates):
                            return True
                    else:
                        if self.solve_finned_fish(digit, house_type, candidates):
                            return True
        return False

    def check_for_hidden_rectangle(self) -> bool:
        """
        If in a rectangle, 2 cells are the only cells that can contain
        a digit in their row and column aside from two other cells
        which can only be that digit or one other digit, those first
        two cells cannot contain the other digit.

        This logic also applies if there is only one cell rather than
        two, in which case we look at its opposite, rather than two
        other cells.
        """
        for rectangle in self.sudoku.rectangles():
            if len({cell.box_num for cell in rectangle}) != 2: continue
            if cells_are_empty(*rectangle) and at_least_one_cell_has_only_two_options(*rectangle):
                if self.solve_hidden_rectangle_pairs(rectangle):
                    return True
                elif self.solve_hidden_rectangle_singles(rectangle):
                    return True
        return False

    def check_for_hidden_tuple(self) -> bool:
        """
        If the only places for n digits appear in n cells in a house,
        then all other options than those digits can be removed from
        those cells.
        """
        sizes = range(2, 5)
        for size, house_type in product(sizes, RCB):
            iter_house = LITERALS[house_type]["iter_house"]
            houses = getattr(self.sudoku, iter_house)
            for house in houses:
                if self.clear_hidden_tuple(house, size):
                    return True
        return False

    def check_for_locked_candidate(self) -> bool:
        """
        If the only places for a digit in a row or column share a
        box, then other cells in that box cannot contain that digit.
        """
        for house_type, digit in product(RC_ITER, range(1, 10)):
            for house in getattr(self.sudoku, house_type):
                cells_with_digit = {cell
                                    for cell in house
                                    if digit in cell}
                if Sudoku.cells_share_a_box(*cells_with_digit):
                    if self.clear_locked_candidate(cells_with_digit, digit):
                        return True
        return False

    def check_for_naked_tuple(self) -> bool:
        """
        If n cells in a house can only contain n different digits, then
        the other cells in that house cannot contain those digits.
        """
        for size, house_type in product(range(2, 5), RCB_ITER):
            for house in getattr(self.sudoku, house_type):
                empty_cells = [cell for cell in house if cell.is_empty]
                candidate_tuples = combinations(empty_cells, r=size)
                for candidate_tuple in candidate_tuples:
                    if self.cells_from_naked_tuple(*candidate_tuple):
                        if self.clear_naked_tuples(house, candidate_tuple):
                            return True
        return False

    def check_for_pointing_rectangle(self) -> bool:
        """
        If a pair of cells could form part of an illegal rectangle, but
        there's a cell in their shared row or column that contains only
        the 2 other digits present in each cell, then any cell that
        sees all three cannot contain those digits.
        """
        for a, b in combinations([cell for cell in self.sudoku if cell.is_empty], r=2):
            if not a.sees(b): continue
            if a.pencil_marks != b.pencil_marks: continue
            if a.y == b.y:
                for key in a.column:
                    c = self.sudoku[key]
                    d = self.sudoku[(b.x, c.y)]
                    digits = self.pointing_rectangle_digits(a, b, c, d)
                    if not digits: continue
                    if self.clear_pointing_rectangle((c, d), digits, "row"):
                        return True
            elif a.x == b.x:
                for key in a.row:
                    c = self.sudoku[key]
                    d = self.sudoku[(c.x, b.y)]
                    digits = self.pointing_rectangle_digits(a, b, c, d)
                    if not digits: continue
                    if self.clear_pointing_rectangle((c, d), digits, "column"):
                        return True
            else:
                continue
        return False

    def check_for_pointing_tuple(self) -> bool:
        """
        If the only cells in a box that can contain a digit share a row
        or column, then other cells in that row or column cannot
        contain that digit.
        """
        for digit, box in product(range(1, 10), self.sudoku.boxes):
            pointing = {cell for cell in box if digit in cell}
            pointed = self.cells_seen_by_pointing_tuple(pointing)
            if self.remove_digits_from_cells(digit, *pointed):
                return True
        return False

    def check_for_skyscraper(self) -> bool:
        """
        If there two rows have a pair of strongly connected cells and
        two of those cells share a column, then any cell which sees
        both cells that don't share a column cannot contain the
        strongly connecting digit. Likewise in the opposite direction.

        This also works if one of the rows has more than two cells, as
        long as all the cells in that row that don't share that column
        share a box.
        """
        for digit, house_type in product(range(1, 10), RC):
            opposite_axis = LITERALS[house_type]["opposite_axis"]
            houses_with_digit = self.sudoku.houses_with_digit(house_type, digit)
            house_pairs = combinations(houses_with_digit, r=2)
            for house_pair in house_pairs:
                a = Sudoku.cells_in_group_with_digits({digit}, house_pair[0])
                b = Sudoku.cells_in_group_with_digits({digit}, house_pair[1])
                pair_house = [house for house in (a, b) if len(house) == 2]
                if not pair_house:
                    continue
                flat_house_pair = {cell for house in (a, b) for cell in house}
                opp_house_nums = {getattr(cell, opposite_axis) for cell in flat_house_pair}
                if self.clear_skyscraper(digit, flat_house_pair, opp_house_nums, opposite_axis):
                    return True
        return False

    def check_for_two_colour_logic(self) -> bool:
        """
        In a chain of strongly connected cells, there are two
        possibilities: either every even cell contains the strongly
        connecting digit, or ever odd cell does. Cells which see at
        least one cell from each colour can therefore not contain the
        digit.
        """
        for digit in range(1, 10):
            strongly_connected_pairs = self.sudoku.strongly_connected_pairs_with_digit(digit)
            if not strongly_connected_pairs: continue
            strongly_connected_chains = self.strongly_connected_cell_chains(strongly_connected_pairs)
            coloured_chains = self.colour_pairs_for_strongly_connected_chains(strongly_connected_chains)
            if self.clear_colour_contradiction(digit, coloured_chains):
                return True
            if self.clear_colour_chain(digit, coloured_chains):
                return True
        return False

    def check_for_unique_rectangle(self) -> bool:
        """
        If a digit can only be in two cells in each of its row and
        column, and those three cells in those rows and columns form a
        rectangle with a fourth cell which contains the same options,
        as its opposite, then the opposite cell cannot contain that
        digit.
        """
        for box in self.sudoku.boxes:
            pairs = [cell for cell in box if len(cell.pencil_marks) == 2]
            for a, b in combinations(pairs, r=2):
                if self.cells_from_naked_tuple(a, b):
                    cell, target = self.unique_rectangle_cell_and_target(a, b)

                    if cell is not None and target is not None:
                        if intersection := cell.pencil_marks.intersection(target.pencil_marks):
                            target.remove(intersection)
                            return True
        return False

    def check_for_xyzwings(self) -> bool:
        """
        If a cell contains only three options and sees two other cells
        which contain only two options and have one digit in common
        with each other and the other digit in common with the first
        cell, then any cell which sees all three cells cannot contain
        the digit shared by all three.
        """
        for index, triple in self.possible_xyzwing_triples():
            if self.clear_xyzwing(index, triple):
                return True
        return False

    def check_for_ywing(self) -> bool:
        """
        If three cells together contain 3 different options, each cell
        contains a different two options, and one of them sees the
        other two, then any cell which sees those other two cannot
        contain their shared digit.
        """
        triples = self.find_ywing_triples()
        if ywings := self.find_valid_ywings(triples):
            for ywing in ywings:
                if self.clear_ywing(ywing):
                    return True
        return False

    # Methods for doing solver logic work

    def clear_colour_contradiction(self, digit: int, coloured_chains):
        for chain_pair in coloured_chains:
            for chain in chain_pair:
                if len(chain) <= 1: continue
                contradiction = max([c_1.sees(c_2) for c_1, c_2 in combinations(chain, r=2)])
                if contradiction:
                    if self.remove_digits_from_cells(digit, *chain):
                        return True
        return False

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

    def clear_colour_chain(self, digit, coloured_chains):
        seen_cells = self.cells_seen_by_colour_chains(coloured_chains)
        if self.remove_digits_from_cells(digit, *seen_cells):
            return True

    @staticmethod
    def clear_hidden_rectangle_pair(digit, pair, pencil_marks):
        operated = False
        removed_digit = next(iter(d for d in pencil_marks if d != digit))
        for focus in pair:
            if focus.remove(removed_digit):
                operated = True
        return operated

    def clear_finned_fish(self, digit, opposite_axis, candidates_cells, perp_group) -> bool:
        """
        Clears digit from pencil marks affected by finned fish. Return
        false if no changes were made.
        """
        flat_proper_fish = {cell for house in perp_group for cell in house}
        proper_fish_perp_house_nums = {getattr(cell, opposite_axis) for cell in flat_proper_fish}
        fin_cells = candidates_cells - flat_proper_fish
        fin_boxes = {cell.box_num for cell in fin_cells}
        non_fin_boxes = {cell.box_num for cell in flat_proper_fish}
        if not fin_boxes.intersection(non_fin_boxes):
            return False

        if len(affected_box_num := {cell.box_num for cell in fin_cells}) == 1:
            affected_box = self.sudoku.box(affected_box_num.pop())
            affected_cells = {cell
                              for cell in affected_box
                              if getattr(cell, opposite_axis) in proper_fish_perp_house_nums
                              and cell not in candidates_cells}
            affected_cells -= {cell
                               for cell in affected_cells
                               if len([f for f in flat_proper_fish if f.sees(cell)]) <= 1}
            if self.remove_digits_from_cells(digit, *affected_cells):
                return True
        return False

    def clear_pointing_rectangle(self, pointing_pair, extra_digits, house) -> bool:
        operated = False
        c, d = pointing_pair
        for pointing in [self.sudoku[key] for key in getattr(c, house)]:
            if pointing.pencil_marks == extra_digits:
                pointed_keys = Cell.intersection(c, d, pointing)
                pointed = [self.sudoku[key] for key in pointed_keys]
                for cell in pointed:
                    cell.remove(pointing.pencil_marks)
                    operated = True
        return operated

    def clear_hidden_rectangle_single(self, digit, focus, opposite) -> bool:
        for house_type in RC:
            check_axis = LITERALS[house_type]["check_axis"]
            single_house = LITERALS[house_type]["single_house"]

            group = {cell
                     for cell in getattr(self.sudoku, single_house)(getattr(opposite, check_axis))
                     if digit in cell}
            if not self.cells_are_strongly_connected_by_digit(digit, *group):
                break
        else:
            digit_to_remove = focus.pencil_marks - {digit}
            if opposite.remove(digit_to_remove):
                return True
        return False

    def clear_hidden_tuple(self, house, size) -> bool:
        for digits in combinations(range(1, 10), r=size):
            candidate_tuple = Sudoku.cells_in_group_with_digits(digits, house)
            if len(candidate_tuple) != size: continue
            if self.cells_form_hidden_tuple(digits, candidate_tuple):
                other_digits = set(range(1, 10)) - set(digits)
                if self.remove_digits_from_cells(other_digits, *candidate_tuple):
                    return True
        return False

    def clear_locked_candidate(self, locked_candidate, digit) -> bool:
        box_num = next(iter(locked_candidate)).box_num
        affected = set(self.sudoku.box(box_num)) - locked_candidate
        if self.remove_digits_from_cells(digit, *affected):
            return True
        return False

    def clear_naked_tuples(self, house, tuple_cells):
        non_members: set[Cell] = set(house) - set(tuple_cells)
        marks = [tuple(cell.pencil_marks) for cell in tuple_cells]
        options = {digit for pms in marks for digit in pms}
        if self.remove_digits_from_cells(options, *non_members):
            return True

    def clear_proper_fish(self, digit: int, fish_cells: set[Cell], perp_house_nums: set[int], house_type: str):
        """
        Clears digit from pencil marks affected by x-wings, swordfish,
        and jellyfish. Return false if no changes were made.
        """
        operated = False
        opposite_house_type = LITERALS[house_type]["opposite_house"]
        for house_num in perp_house_nums:
            house = getattr(self.sudoku, opposite_house_type)(house_num)
            affected_cells = {cell for cell in house if cell not in fish_cells}
            if self.remove_digits_from_cells(digit, *affected_cells):
                operated = True
        return operated

    def clear_skyscraper(self, digit, cells, house_nums, axis) -> bool:
        for house_num in house_nums:
            if len(base := {cell
                            for cell in cells
                            if getattr(cell, axis) == house_num}) == 2:
                skyscrapers = cells - base
                affected_keys = Cell.intersection(*skyscrapers)
                affected_cells = {self.sudoku[key] for key in affected_keys}
                if self.remove_digits_from_cells(digit, *affected_cells):
                    return True
        return False

    def clear_xyzwing(self, index, triple):
        shared_digit = self.xyzwing_triple_shared_digit(index, triple)
        affected_cells = self.xyzwing_affected_cells(shared_digit, triple)
        if self.remove_digits_from_cells(shared_digit, *affected_cells):
            return True
        return False

    def cells_are_strongly_connected_by_digit(self, digit: int, *cells: Cell) -> bool:
        """
        Return whether input cells are the only two cells in their
        row, or column that can be digit.
        """
        if len(cells) != 2:
            return False
        if Sudoku.cells_share_a_column(*cells):
            axis = "x"
            house_type = "column"
        elif Sudoku.cells_share_a_row(*cells):
            axis = "y"
            house_type = "row"
        elif Sudoku.cells_share_a_box(*cells):
            axis = "house_num"
            house_type = "box"
        else:
            return False
        return len([
            cell
            for cell in getattr(self.sudoku, house_type)(getattr([*cells][0], axis))
            if digit in cell
        ]) == 2

    @staticmethod
    def cells_form_hidden_tuple(digits, candidate_tuple) -> bool:
        """
        If input cells individually contain two of input digits and
        together contain all three digits, then they are a hidden tuple.
        """
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
    def cells_from_naked_tuple(*cells) -> bool:
        """Return whether input cells cumulatively contain exactly as
        many possible digits as there are input cells."""
        pencil_marks = [cell.pencil_marks for cell in cells]
        flattened_pms = {digit for house in pencil_marks for digit in house}
        if len(set.union(flattened_pms)) != len(cells):
            return False
        return True

    def cells_seen_by_colour_chains(self, colour_chains: list[list[list[Cell]]]) -> set[Union[Cell, Any]]:
        """
        Return cells which are seen by two or more cells of different
        colours from colour chains.
        :param colour_chains: Lists of cells separated by their colour
        """
        result = set()
        for chain_pair in colour_chains:
            for seer_pair in product(*chain_pair):
                seen = {self.sudoku[key] for key in Cell.intersection(*seer_pair)}
                result.update({cell for cell in seen if cell.is_empty})
        return result

    def cells_seen_by_pointing_tuple(self, pointing: set[Cell]) -> set[Cell]:
        """
        Return cells in the row or column that all cells in pointing
        share, minus the cells in pointing. If no such row or column
        exists, return an empty set.
        :param pointing: Set of cells that share a box and digit.
        :return: Set of cells that share a row or column and a digit.
        """
        if Sudoku.cells_share_a_row(*pointing):
            pointed = set(self.sudoku.row(next(iter(pointing)).y))
        elif Sudoku.cells_share_a_column(*pointing):
            pointed = set(self.sudoku.column(next(iter(pointing)).x))
        else:
            return set()
        pointed -= pointing
        return pointed

    @staticmethod
    def colour_pairs_for_strongly_connected_chains(chains: list[list[Cell]]) -> list[list[list[Cell]]]:
        """
        Separates each chain in chains into its odd and even elements.
        :param chains: List of chains of strongly connected cells.
        """
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

    @staticmethod
    def find_empty_rectangle_house(house_type, rectangle) -> int:
        """
        Return the house_num that the cells which share a row or column in
        an empty rectangle box share.
        """
        a = {0, 1, 2}
        b = {3, 4, 5}
        c = {6, 7, 8}
        check_axis = LITERALS[house_type]["check_axis"]

        house_nums = {getattr(cell, check_axis) for cell in rectangle}
        for num_set in a, b, c:
            if len(num := (num_set - house_nums)) == 1:
                return num.pop()

    def find_empty_rectangle_perp_sc_cell(self, row_num: int, column_num: int, digit: int) -> Optional[Cell]:
        """
        Return the cell in a strongly connected pair with a cell seen
        by a cell that lies in an empty rectangle's row or column that
        lies in the empty rectangle's other column or row. If no such
        cell exists, returns None.
        """
        rectangle_box_num = self.sudoku[column_num, row_num].box_num
        for house_type in "row", "column":
            check_axis = LITERALS[house_type]["check_axis"]
            single_house = LITERALS[house_type]["single_house"]
            opposite_axis = LITERALS[house_type]["opposite_axis"]
            opposite_house = LITERALS[house_type]["opposite_house"]
            er_house_num = row_num if house_type == "row" else column_num
            er_opp_house_num = column_num if house_type == "row" else row_num
            digit_cells = {cell
                           for cell in getattr(self.sudoku, house_type)(er_house_num)
                           if digit in cell and cell not in self.sudoku.box(rectangle_box_num)}
            for cell_1 in digit_cells:
                perp_group = {cell
                              for cell in getattr(self.sudoku, opposite_house)(getattr(cell_1, opposite_axis))
                              if digit in cell and cell not in self.sudoku.box(rectangle_box_num)}
                for cell_2 in perp_group:
                    contra_perp_group = {cell
                                         for cell in getattr(self.sudoku, single_house)(getattr(cell_2, check_axis))
                                         if digit in cell}
                    if len(contra_perp_group) != 2:
                        continue
                    if min([cell.box_num == er_house_num for cell in contra_perp_group]):
                        continue
                    contra_cell = next(iter(contra_perp_group - {cell_2}))
                    if contra_cell in self.sudoku.box(rectangle_box_num):
                        continue
                    if getattr(contra_cell, opposite_axis) == er_opp_house_num:
                        return cell_1
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

    def find_ywing_triples(self) -> list[tuple[Cell, Cell, Cell]]:
        """
        Return a list of tuples of cells in self.sudoku which meet
        the following criteria:

        - there are three cells in the tuple;
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

    def clear_ywing(self, ywing) -> bool:
        operated = False
        wing_a, wing_b = ywing
        shared_digit: int = wing_a.pencil_marks.intersection(wing_b.pencil_marks).pop()
        affected_cells = {cell for cell in self.sudoku
                          if (cell.sees(wing_a) and cell.sees(wing_b))}
        if self.remove_digits_from_cells(shared_digit, *affected_cells):
            return True
        return operated

    def match_endpoints_with_adjacencies(self, adjacencies, endpoints):
        """
        Match each endpoint cell with adjacent cells and return the
        results after pruning duplicates.
        """
        chains = [[cell] for cell in endpoints]
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

    @staticmethod
    def pointing_rectangle_digits(a: Cell, b: Cell, c: Cell, d: Cell) -> set:
        """
        Return digits, if any, that are in a pointing rectangle made up of
        input cells.
        """
        if c.is_empty:
            if c.pencil_marks.issuperset(a.pencil_marks):
                if d.is_empty:
                    if d.pencil_marks.issuperset(b.pencil_marks):
                        return set.union(
                            *[c.pencil_marks - a.pencil_marks, d.pencil_marks - a.pencil_marks]
                        )

    def possible_xyzwing_triples(self) -> Generator[tuple[int, [Cell, Cell, Cell]], None, None]:
        """
        Yields cells which form an xyzwing and the digit that connects
        them.
        :return: digit, tuple(cells which form an xyzwing with digit)
        """
        for triple in combinations(self.sudoku, r=3):
            if len({cell.box_num for cell in triple}) != 2:
                continue

            indices = set(range(3))
            for i in range(3):
                axis = triple[i]
                wings = [triple[x] for x in indices - {i}]
                if len(axis.pencil_marks) == 3 and len(wings[0].pencil_marks) == len(wings[1].pencil_marks) == 2:
                    yield i, triple

    def potential_avoidable_rectangles(self) -> Generator[tuple[Cell, Cell, Cell, Cell], None, None]:
        """
        Yield groups of 4 cells which form a rectangle and could lead
        to a sudoku with more than one correct solution.
        """
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

    @staticmethod
    def remove_digits_from_cells(digits: Union[int, Iterable[int]], *cells: Cell) -> bool:
        """
        Removes digits from cells if the digits exist.
        Returns False if no changes were made.
        """
        operated = False
        for cell in cells:
            if cell.remove(digits):
                operated = True
        return operated

    @staticmethod
    def remove_duplicate_chains(chains: list[list[Cell]]) -> None:
        """Remove colour_chains from the input that are either too short or
        (perhaps reversed) duplicates."""
        for x, y in combinations(chains, r=2):
            if len(x) == len(y):
                if x in chains and len(x) <= 2:
                    chains.remove(x)
                if y in chains and x == y[::-1]:
                    chains.remove(y)

    def solve_finned_fish(self, digit: int, house_type: str, candidates: list[list[Cell]]) -> bool:
        """
        Checks for finned x-wings, swordfish, and jellyfish on digit in candidates.
        """
        opposite_axis = LITERALS[house_type]["opposite_axis"]
        check_axis = LITERALS[house_type]["check_axis"]
        size = len(candidates)
        candidates_cells = {cell for house in candidates for cell in house}
        fish_perp_house_nums = {getattr(cell, opposite_axis) for cell in candidates_cells}
        fish_by_perp_house = [
            [cell for cell in candidates_cells
             if getattr(cell, opposite_axis) == house_num]
            for house_num in fish_perp_house_nums
        ]
        perp_candidate_groups = combinations(fish_by_perp_house, r=size)
        for perp_group in perp_candidate_groups:
            if len({getattr(cell, check_axis) for house in perp_group for cell in house}) != size:
                continue
            if self.clear_finned_fish(digit, opposite_axis, candidates_cells, perp_group):
                return True
        return False

    def solve_hidden_rectangle_pairs(self, rectangle) -> bool:
        for house_type, pair in product(RC, combinations(rectangle, r=2)):
            check_axis = LITERALS[house_type]["check_axis"]

            if cells_share_axis(check_axis, *pair) and self.cells_from_naked_tuple(*pair):
                pencil_marks = pair[0].pencil_marks
                opposite_pair: set[Cell, Cell] = {*rectangle} - {*pair}
                if all_cells_in_house_contain_pencil_marks(opposite_pair, pencil_marks) is False:
                    continue
                for digit in pencil_marks:
                    if self.cells_are_strongly_connected_by_digit(digit, *opposite_pair):
                        if self.clear_hidden_rectangle_pair(digit, opposite_pair, pencil_marks):
                            return True

    def solve_hidden_rectangle_singles(self, rectangle):
        for check_cell in rectangle:
            pencil_marks = check_cell.pencil_marks
            if len(pencil_marks) == 2:
                house = {*rectangle} - {check_cell}
                if all_cells_in_house_contain_pencil_marks(house, pencil_marks):
                    opposite = {cell
                                for cell in rectangle
                                if cell.x != check_cell.x and cell.y != check_cell.y}.pop()
                    for digit in pencil_marks:
                        if self.clear_hidden_rectangle_single(digit, check_cell, opposite):
                            return True
        return False

    def solve_proper_fish(self, digit: int, house_type: str, candidates: list[list[Cell]]) -> bool:
        """
        Checks for x-wings, swordfish, and jellyfish on digit in candidates.
        """
        size = len(candidates)
        fish_cells = {cell for group in candidates for cell in group}
        opposite_axis = LITERALS[house_type]["opposite_axis"]
        perpendicular_house_nums = {getattr(cell, opposite_axis) for cell in fish_cells}
        if len(perpendicular_house_nums) == size:
            return self.clear_proper_fish(digit, fish_cells, perpendicular_house_nums, house_type)
        return False

    def strongly_connected_cell_chains(self, pairs: set[tuple[Cell, Cell]]):
        """
        Return a list of lists of cells which form a chain of three or
        more cells that are strongly connected.
        """
        adjacencies: dict = self.strongly_connected_chain_adjacent_cells(pairs)
        endpoints = {k for k, v in adjacencies.items() if len(v) == 1}
        return self.match_endpoints_with_adjacencies(adjacencies, endpoints)

    @staticmethod
    def strongly_connected_chain_adjacent_cells(pairs) -> dict[Cell, set[Cell]]:
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

    @staticmethod
    def trimmed_fish_houses(candidate_houses, house_type, size) -> Optional[tuple]:
        """Return group of cells that could be an xwing, swordfish, or jellyfish."""
        opposite_axis = LITERALS[house_type]["opposite_axis"]
        for candidates in combinations(candidate_houses, r=size):
            total_axes = set()
            for line in candidates:
                total_axes.update([getattr(cell, opposite_axis) for cell in line])
            if len(total_axes) == size:
                return candidates
        return None

    def unique_rectangle_cell_and_target(self, a, b) -> tuple[Optional[Cell], Optional[Cell]]:
        """Given cell_a, cell_b that share a row or column in the same box
        and have identical pencil_marks, return a cell (if any) that shares a
        column or row (respectively) with one of them and the cell that
        completes the rectangle."""
        if a.y == b.y:
            cell, target = self.unique_rectangle_cell_and_target_share_a_row(a, b)
        elif a.x == b.x:
            cell, target = self.unique_rectangle_cell_and_target_share_a_column(a, b)
        else:
            return None, None
        return cell, target

    def unique_rectangle_cell_and_target_share_a_column(self, a, b) -> tuple[Cell, Cell]:
        final_cell = None
        target = None
        for cell in [self.sudoku[k] for k in a.row if k != a.coordinates]:
            if cell.pencil_marks == a.pencil_marks:
                target = self.sudoku[(cell.x, b.y)]
                final_cell = cell
                break
        else:
            for cell in [self.sudoku[k] for k in b.row if k != b.coordinates]:
                if cell.pencil_marks == a.pencil_marks:
                    target = self.sudoku[(cell.x, a.y)]
                    final_cell = cell
                    break
        return final_cell, target

    def unique_rectangle_cell_and_target_share_a_row(self, a, b) -> tuple[Cell, Cell]:
        final_cell = None
        target = None
        for cell in [self.sudoku[k] for k in a.column if k != a.coordinates]:
            if cell.pencil_marks == a.pencil_marks:
                target = self.sudoku[(b.x, cell.y)]
                final_cell = cell
                break
        else:
            for cell in [self.sudoku[k] for k in b.column if k != b.coordinates]:
                if cell.pencil_marks == b.pencil_marks:
                    target = self.sudoku[(a.x, cell.y)]
                    final_cell = cell
                    break
        return final_cell, target

    @staticmethod
    def x_wing_if_it_has_fins(fin_house, x_wing_house) -> list:
        """Return the x-wing hidden inside a finned x-wing if such an x-wing exists."""
        for fin_0, fin_1 in combinations(fin_house, r=2):
            checktangle = [
                x_wing_house[0],
                fin_0,
                x_wing_house[1],
                fin_1
            ]
            if Sudoku.cells_form_a_rectangle(*checktangle):
                return checktangle
        return []

    def xyzwing_affected_cells(self, shared_digit: int, triple: tuple[Cell, Cell, Cell]) -> list:
        """
        Return cells which contain shared_digit and see all three cells
        in triple.
        """
        affected_cells = []
        if affected_keys := set.intersection(*[cell.visible_cells() for cell in triple]):
            for key in affected_keys:
                cell = self.sudoku[key]
                if shared_digit in cell:
                    affected_cells.append(cell)
        return affected_cells

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


def at_least_one_cell_has_only_two_options(*cells) -> bool:
    return bool([cell
                 for cell in cells
                 if len(cell.pencil_marks) == 2])


def cells_are_empty(*cells) -> bool:
    """Return whether each cell in cells is empty."""
    return min([cell.is_empty for cell in cells])


def cells_share_axis(check_axis, *cells: Cell) -> bool:
    """Return whether input cells all share a row or column.
    check_axes should be 'x' for column or 'y' for row."""
    axes = {getattr(cell, check_axis) for cell in cells}
    return len(axes) == 1


def all_cells_in_house_contain_pencil_marks(house: Iterable[Cell], pencil_marks: set[int]) -> bool:
    """Return whether all cells in cells contain each digit in pencil_marks."""
    return min([
        cell.pencil_marks.issuperset(pencil_marks)
        for cell in house
    ])


def list_diff(checked_against: list, check_list: list) -> list:
    """
    Return a list containing all elements in checked_against that
    don't appear in check_list. Duplicates matter.
    """
    copy_against = copy(checked_against)
    copy_list = copy(check_list)
    difference = []
    for item in checked_against:
        copy_against.remove(item)
        if item in copy_list:
            copy_list.remove(item)
        else:
            difference.append(item)
    return difference
