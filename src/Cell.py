import itertools


class Cell:
    def __init__(self, coordinates: tuple):
        self.coordinates = coordinates
        self.x = coordinates[1]
        self.y = coordinates[0]
        self.digit = " "

    def __repr__(self):
        return f"Cell({self.coordinates}: {self.digit})"

    def __eq__(self, other):
        if self.digit == other.digit:
            return True
        return False

    def __ne__(self, other):
        if self.digit == other.digit:
            return False
        return True
        
    @property
    def is_empty(self):
        return self.digit == " "
        
    @property
    def box(self):
        x = self.x - self.x % 3
        y = self.y - self.y % 3
        boxes = [(y+i, x+j) for i, j in itertools.product(range(3), repeat=2)]
        return boxes
        
    @property
    def row(self):
        return [(self.y, i) for i in range(9)]

    @property
    def column(self): 
        return [(i, self.x) for i in range(9)]
        
    def fill(self, digit: int):
        self.digit = digit if digit == " " else int(digit)
        
    def clear(self):
        self.digit = " "
