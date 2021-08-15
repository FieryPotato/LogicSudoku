import itertools
from typing import Union


RANGE_SET = {i for i in range(1, 10)}


class Cell:
    def __init__(self, coordinates: tuple[int, int]) -> None:
        self.coordinates: tuple = coordinates
        self.x: int = coordinates[1]
        self.y: int = coordinates[0]
        self.digit: Union[int, str] = " "
        self.pencil_marks = RANGE_SET

    def __repr__(self) -> str:
        return f"Cell({self.coordinates}: {self.digit})"

    def __eq__(self, other) -> bool:
        if self.digit == other.digit:
            return True
        return False

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
        boxes = [(y+i, x+j) for i, j in itertools.product(range(3), repeat=2)]
        return boxes
        
    @property
    def row(self) -> list:
        return [(i, self.y) for i in range(9)]

    @property
    def column(self) -> list:
        return [(self.x, i) for i in range(9)]
        
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

    def copy(self) -> "Cell":
        new_cell = Cell(self.coordinates)
        new_cell.fill(self.digit)
        return new_cell
