import itertools
from typing import Union

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
    def __init__(self, coordinates: tuple[int, int]) -> None:
        self.coordinates: tuple = coordinates
        self.x: int = coordinates[0]
        self.y: int = coordinates[1]
        self.digit: Union[int, str] = " "
        self.pencil_marks = {i for i in range(1, 10)}

    def __repr__(self) -> str:
        return f"Cell({self.coordinates}: {self.digit})"

    def __eq__(self, other) -> bool:
        for attribute in ("coordinates", "digit", "pencil_marks"):
            if getattr(self, attribute) == getattr(other, attribute):
                continue
            else:
                return False
        return True

    def __ne__(self, other) -> bool:
        if self.digit == other.digit:
            return False
        return True

    @property
    def is_empty(self) -> bool:
        return self.digit == " "

    @property
    def box(self) -> list:
        x = self.x - self.x % 3
        y = self.y - self.y % 3
        boxes = [(x + i, y + j) for i, j in itertools.product(range(3), repeat=2)]
        return boxes

    @property
    def row(self) -> list:
        return [(i, self.y) for i in range(9)]

    @property
    def column(self) -> list:
        return [(self.x, i) for i in range(9)]

    @property
    def box_num(self) -> int:
        for key, box in BOX_MAP.items():
            if self.coordinates in box:
                return key

    def fill(self, digit: Union[int, str]) -> None:
        if digit == " ":
            self.digit: str = digit
        else:
            self.digit: int = int(digit)
            self.pencil_marks: set = set()
        return None

    def clear(self) -> None:
        self.digit = " "
        return None
