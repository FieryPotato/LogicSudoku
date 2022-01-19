import itertools

from typing import Generator

BOX_MAP: dict = {
    0: ((0, 0), (1, 0), (2, 0),
        (0, 1), (1, 1), (2, 1),
        (0, 2), (1, 2), (2, 2)),
    1: ((3, 0), (4, 0), (5, 0),
        (3, 1), (4, 1), (5, 1),
        (3, 2), (4, 2), (5, 2)),
    2: ((6, 0), (7, 0), (8, 0),
        (6, 1), (7, 1), (8, 1),
        (6, 2), (7, 2), (8, 2)),
    3: ((0, 3), (1, 3), (2, 3),
        (0, 4), (1, 4), (2, 4),
        (0, 5), (1, 5), (2, 5)),
    4: ((3, 3), (4, 3), (5, 3),
        (3, 4), (4, 4), (5, 4),
        (3, 5), (4, 5), (5, 5)),
    5: ((6, 3), (7, 3), (8, 3),
        (6, 4), (7, 4), (8, 4),
        (6, 5), (7, 5), (8, 5)),
    6: ((0, 6), (1, 6), (2, 6),
        (0, 7), (1, 7), (2, 7),
        (0, 8), (1, 8), (2, 8)),
    7: ((3, 6), (4, 6), (5, 6),
        (3, 7), (4, 7), (5, 7),
        (3, 8), (4, 8), (5, 8)),
    8: ((6, 6), (7, 6), (8, 6),
        (6, 7), (7, 7), (8, 7),
        (6, 8), (7, 8), (8, 8))
}


class Cell:

    def __init__(self, coordinates: tuple[int, int], digit=" ") -> None:
        self.coordinates: tuple = coordinates
        self.x: int = coordinates[0]
        self.y: int = coordinates[1]
        self.digit: int | str = digit
        self.pencil_marks: set[int] = {i for i in range(1, 10)}
        self.started_empty: bool = True

    def __repr__(self) -> str:
        return f"Cell({self.coordinates}: {self.digit})"

    def __hash__(self):
        return hash(self.coordinates)

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__): return False
        for attribute in ("coordinates", "digit", "pencil_marks", "started_empty"):
            if getattr(self, attribute) != getattr(other, attribute):
                return False
        return True

    def __ne__(self, other) -> bool:
        if not isinstance(other, self.__class__): return False
        for attribute in ("coordinates", "digit", "pencil_marks", "started_empty"):
            if getattr(self, attribute) != getattr(other, attribute):
                return True
        return False

    def __bool__(self) -> bool:
        return not self.is_empty

    def __iter__(self) -> Generator[int, None, None]:
        """Iterates through cell pencil_marks."""
        for digit in self.pencil_marks:
            yield digit

    def __contains__(self, digit) -> bool:
        """Return whether digit is in pencil_marks."""
        return digit in self.pencil_marks

    def __add__(self, other) -> int:
        s_digit = 0 if self.is_empty else self.digit
        o_digit = 0 if other.is_empty else other.digit
        return s_digit + o_digit

    def __sub__(self, other) -> int:
        s_digit = 0 if self.is_empty else self.digit
        o_digit = 0 if other.is_empty else other.digit
        return s_digit - o_digit

    def __mul__(self, other) -> int:
        s_digit = 0 if self.is_empty else self.digit
        o_digit = 0 if other.is_empty else other.digit
        return s_digit * o_digit

    def __int__(self) -> int:
        if self.is_empty:
            return 0
        assert isinstance(self.digit, int)
        return self.digit

    @property
    def is_empty(self) -> bool:
        return self.digit == " "

    @property
    def box(self) -> list[tuple[int, int]]:
        """Return a list containing the keys of other cells in the same box."""
        x = self.x - self.x % 3
        y = self.y - self.y % 3
        boxes = [(x + i, y + j) for i, j in itertools.product(range(3), repeat=2)]
        return boxes

    @property
    def row(self) -> list[tuple[int, int]]:
        """Return a list containing the keys of other cells in the same row."""
        return [(i, self.y) for i in range(9)]

    @property
    def column(self) -> list[tuple[int, int]]:
        """Return a list containing the keys of other cells in the same column."""
        return [(self.x, i) for i in range(9)]

    @property
    def box_num(self) -> int:
        """Return this cell's ordinal box number."""
        for key, box in BOX_MAP.items():
            if self.coordinates in box:
                return key

    @property
    def row_num(self) -> int:
        """Return this cell's ordinal row number."""
        return self.y

    @property
    def col_num(self) -> int:
        """Return this cell's ordinal column number."""
        return self.x

    def fill(self, digit: int | str) -> None:
        """Fill the cell with digit and updates pencil_marks."""
        if digit == " ":
            self.digit: str = digit
            return
        digit = int(digit)
        if digit == 0:
            self.digit: str = " "
        else:
            if digit <= 0 or digit >= 10:
                raise ValueError(f"{digit} must be between 1 and 9 (inclusive).")
            self.digit: int = digit
            self.pencil_marks: set = {digit}
        return

    def clear(self) -> None:
        """Empty the cell."""
        self.digit = " "
        self.pencil_marks = {i for i in range(1, 10)}
        return

    def has_same_options_as(self, other: "Cell") -> bool:
        """Return whether this cell's pencil_marks are identical to other's."""
        return self.pencil_marks == other.pencil_marks

    @property
    def number_of_options(self) -> int:
        """Return the number of pencil_marks."""
        return len(self.pencil_marks)

    def visible_cells(self, *args: str) -> set[tuple[int, int]]:
        """Return a set containing keys of each cell visible from this
        one (not including itself). Can enter ."""
        if not args:
            houses = "row", "column", "box"
        else:
            houses = args
        keys = set()
        for house_type in houses:
            house = getattr(self, house_type)
            keys.update(house)
        keys.remove(self.coordinates)
        return keys

    def sees(self, other: "Cell") -> bool:
        """Return whether self sees other in row, column, or box and self and
         other are different cells."""
        if self.coordinates == other.coordinates:
            return False
        return max(self.x == other.x,
                   self.y == other.y,
                   self.box_num == other.box_num)

    def remove(self, pencil_marks: set | int | list) -> bool:
        """Remove input set from self.pencil_marks;
        return True if a change was made, and False if not."""
        if type(pencil_marks) in (list, tuple, int):
            pencil_marks = {pencil_marks}
        if self.pencil_marks.intersection(pencil_marks):
            self.pencil_marks -= pencil_marks
            return True
        return False

    def intersection(*args: "Cell") -> set[tuple[int, int]]:
        """
        Return a set of keys of all cells which see each of the input
        cells.
        """
        seen_keys = [cell.visible_cells() for cell in args]
        return set.intersection(*seen_keys)
