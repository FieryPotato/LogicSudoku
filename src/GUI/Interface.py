import json
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from src.Sudoku import Sudoku
from src.Cell import Cell

PENCILMARK = ("Menlo", "14")
DIGIT = ("Menlo", "51")


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("750x645")
        self.title("Sudoku")
        self.resizable(width=False, height=False)
        self.sudoku = tk_Sudoku(parent=self)
        self.sudoku.grid(row=0, column=0, columnspan=2)
        fill_button = tk.Button(self, text="Load", command=self.sudoku.new_sudoku)
        fill_button.grid(row=1, column=0)
        quit_button = tk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=1, column=1)


class tk_Sudoku(tk.Frame):
    """Represents and displays a Sudoku in the GUI."""

    def __init__(self, parent=None, cnf={}, **kwargs):
        super().__init__(parent, cnf)
        self.parent = parent
        self.controller = parent
        self.children = {}
        self.sudoku: Sudoku = Sudoku()
        self.cell_dict: dict = {}
        self.new_sudoku(init=True)
        span = 19
        box_borders = {0, 6, 12, 18}
        tk_cell: tk_Cell
        for tk_cell in self.cell_dict.values():
            x = tk_cell.x * 2
            y = tk_cell.y * 2
            cell_x = x + 1
            cell_y = y + 1
            if x in box_borders:
                pass
            else:
                vert_sep = ttk.Separator(self, orient="vertical")
                vert_sep.grid(row=0, column=x, rowspan=span, sticky="ns")
            if y in box_borders:
                pass
            else:
                hor_sep = ttk.Separator(self, orient="horizontal")
                hor_sep.grid(row=y, column=0, columnspan=span, sticky="ew")
            tk_cell.grid(row=cell_y, column=cell_x)
        for i in box_borders:
            vert_sep = tk.Frame(self, bd=5, width=3, background="black")
            vert_sep.grid(row=0, column=i, rowspan=span, sticky="ns")
            hor_sep = tk.Frame(self, bd=5, height=3, background="black")
            hor_sep.grid(row=i, column=0, columnspan=span, sticky="ew")

    def new_sudoku(self, init=False) -> None:
        if init:
            self.sudoku = Sudoku()
            for k, v in self.sudoku.cell_dict.items():
                self.cell_dict[k] = tk_Cell(v.coordinates, parent=self, controller=self.controller)
        else:
            self.sudoku = load_puzzle()
            for k, v in self.cell_dict.items():
                v.update_frames()

    def __getattr__(self, item):
        """Allows us to treat this window as the actual sudoku
        when convenient."""
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            return getattr(self.sudoku, item)


class tk_Cell(tk.Frame):
    """Represents and displays Cells in the GUI."""

    def __init__(self, key: tuple[int, int], parent: tk_Sudoku = None,
                 controller: Application = None, cnf={}, **kwargs):
        super().__init__(parent, cnf, **kwargs)
        self.parent = parent
        self.controller = controller
        self.key = key
        self.frames = {}
        for F in tk_PencilMarks, tk_Digit:
            name = F.__name__
            frame = F(parent=self, controller=self.controller)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.update_frames()

    def __getattr__(self, item):
        """Allows us to treat these representations as the actual cells
        they're meant to represent when convenient (as long as nothing
        clashes)."""
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            return getattr(self.cell, item)

    def update_frames(self) -> None:
        if self.is_empty:
            self.show_frame("tk_PencilMarks")
        else:
            self.show_frame("tk_Digit")

    def show_frame(self, frame_name) -> None:
        frame = self.frames[frame_name]
        frame.tkraise()
        frame.update_values()

    @property
    def cell(self) -> Cell:
        """Return the cell object that this frame represents."""
        return self.parent.sudoku.cell_dict[self.key]


class tk_PencilMarks(tk.Frame):
    """Represents and displays pencil marks in a cell."""

    def __init__(self, parent: tk_Cell = None, controller: Application = None,
                 cnf={}, **kwargs):
        super().__init__(parent, cnf, **kwargs)
        self.controller = controller
        self.parent = parent
        self.pm_dict: dict = {}
        for i in range(1, 10):
            text_var = tk.StringVar(master=self, value=self.text_var_value(i),
                                    name=f"{parent.coordinates} - {i} PM")
            self.pm_dict[i] = {
                "text": text_var,
                "label": tk.Label(master=self, textvariable=text_var, font=PENCILMARK)
            }
            pm_key: str = _ternary(i - 1) if i != 1 else "0"
            assert len(coordinates := f"{int(pm_key):02d}") == 2
            y, x = coordinates
            self.pm_dict[i]["label"].grid(row=y, column=x)

    def text_var_value(self, digit) -> str:
        if digit in self.parent.pencil_marks:
            return digit
        return " "

    def update_values(self) -> None:
        for digit, values in self.pm_dict.items():
            values["text"].set(self.text_var_value(digit))


class tk_Digit(tk.Frame):
    """Represents and displays digits in a cell."""

    def __init__(self, parent: tk_Cell = None, controller: Application = None,
                 cnf={}, **kwargs):
        super().__init__(parent, cnf, **kwargs)
        self.parent = parent
        self.controller = controller
        self.text = tk.StringVar(master=self, value=self.digit(),
                                 name=f"{parent.coordinates} Digit")
        self.label = tk.Label(master=self, textvariable=self.text, font=DIGIT)
        self.label.pack()

    def update_values(self) -> None:
        self.text.set(self.digit())

    def digit(self) -> str:
        return self.parent.digit


def load_puzzle() -> Sudoku:
    path: str = filedialog.askopenfilename(
        title="Select a file", filetypes=(("JSON files", "*.json"), ("text files", "*.txt"))
    )
    try:
        with open(path, "r") as file:
            if path.endswith(".txt"):
                contents = file.read()
                return Sudoku.from_string(contents)
            elif path.endswith(".json"):
                contents = json.load(file)
                return Sudoku.from_json(contents)
            else:
                raise ValueError(f"File {path} does not have a supported file type. "
                                 f"Please use .txt or .json.")
    except FileNotFoundError as e:
        return e


def _ternary(number: int) -> str:
    """Convert a decimal number to ternary."""
    quotient = number / 3
    remainder = number % 3
    if quotient == 0:
        return ""
    else:
        return _ternary(int(quotient)) + str(int(remainder))


def _test():
    Application().mainloop()


if __name__ == "__main__":
    _test()
