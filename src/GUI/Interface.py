import json
from tkinter import *
from tkinter import filedialog

from src.Sudoku import Sudoku
from src.Cell import Cell


class Application(Frame):
    """Represents and displays a Sudoku in the GUI."""
    def __init__(self, root):
        super().__init__()
        self.puzzle: Sudoku = Sudoku()
        self.cell_dict: dict = {}
        self.new_sudoku(init=True)
        value: tk_Cell
        for value in self.cell_dict.values():
            x = value.x
            y = value.y
            value.grid(row=y, column=x)

    def new_sudoku(self, init=False) -> None:
        if init:
            self.puzzle = Sudoku()
        else:
            self.puzzle = load_puzzle()
        self.cell_dict = {k: tk_Cell(self.puzzle, v.coordinates, master=self) for k, v in self.puzzle.cell_dict.items()}


class tk_Cell(Frame):
    """Represents and displays Cells in the GUI."""
    def __init__(self, sudoku, key, master, cnf={}, **kwargs):
        super().__init__(master, cnf)
        self.data: Cell = sudoku[key]
        self.digit_label = tk_Digit(master=self)
        self.pm_frame = tk_PencilMarks(master=self)

    def __getattr__(self, item):
        """Allows us to treat these representations as the actual cells
        they're meant to represent when convenient."""
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            return getattr(self.data, item)


class tk_PencilMarks(Frame):
    """Represents and displays pencil marks in a cell."""
    def __init__(self, master: tk_Cell = None, cnf={}, **kwargs):
        super().__init__(master, cnf)
        self.data = master.pencil_marks
        self.pm_dict = {}
        for i in range(1, 10):
            self.pm_dict[i] = {
                "empty": bool(i in self.data),
                "label": Label(master=self),
                "text": StringVar()
            }
            self.pm_dict[i]["label"].config(text=self.pm_dict[i]["text"])

        for k, v in self.pm_dict.items():
            label = self.pm_dict[k]["label"]
            pm_key = _ternary(k - 1) if k != 1 else "0"
            assert len(coordinates := f"{int(pm_key):02d}") == 2
            y, x = coordinates
            label.grid(row=y, column=x)


class tk_Digit(Frame):
    """Represents and displays digits in a cell."""
    def __init__(self, master: tk_Cell = None, cnf={}, **kwargs):
        super().__init__(master, cnf)
        self.data = master.digit


def load_puzzle() -> Sudoku:
    path: str = filedialog.askopenfilename(
        title="Select a file", filetypes=(("JSON files", "*.json"), ("text files", "*.txt"))
    )
    with open(path, "r") as file:
        if path.endswith(".txt"):
            contents = file.read()
            return Sudoku.from_string(contents)
        elif path.endswith(".json"):
            contents = json.load(file)
            return Sudoku.from_json(contents)
        else:
            raise ValueError(f"File {path} is not a valid file type. Please use .txt or .json.")


def _ternary(number: int) -> str:
    """Convert a decimal number to ternary."""
    quotient = number / 3
    remainder = number % 3
    if quotient == 0:
        return ""
    else:
        return _ternary(int(quotient)) + str(int(remainder))



def _test():
    root = Tk()
    test = Application(root)
    test.grid(row=0, rowspan=2)
    fill_button = Button(root, text="Fill", command=load_puzzle)
    fill_button.grid(row=1, column=0)
    quit_button = Button(root, text="QUIT", command=root.destroy)
    quit_button.grid(row=1, column=1)
    root.mainloop()


if __name__ == "__main__":
    _test()