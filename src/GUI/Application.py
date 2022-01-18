import json
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from src.Solver import Solver
from src.Sudoku import Sudoku
from src.Cell import Cell

PENCILMARK = ("Menlo", "14")
DIGIT = ("Menlo", "51")


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("750x750")
        self.title("Sudoku")
        self.resizable(width=False, height=False)
        self.sudoku = tk_Sudoku(parent=self)

        self.buttons = {
            "clear": tk.Button(self, text="Clear Grid", command=self.sudoku.reset),
            "load": tk.Button(self, text="Load", command=self.sudoku.new_sudoku),
            "solve": tk.Button(self, text="Solve", command=self.sudoku.solve),
            "step": tk.Button(self, text="Step", command=self.sudoku.step),
            "update_pm": tk.Button(self, text="Update Pencil Marks", command=self.sudoku.update_pms),
            "quit": tk.Button(self, text="Quit", command=self.destroy)
        }

        self.step_label = tk.StringVar()
        self.solution_labels = {
            "solved": tk.Label(self, text="Solve Successful."),
            "unsolved": tk.Label(self, text="Solve Unsuccessful"),
            "message": tk.Label(self, textvariable=self.step_label)
        }

        self.sudoku.grid(row=0, column=0, rowspan=len(self.buttons), sticky="nsew")
        for i, button in enumerate(self.buttons):
            self.buttons[button].grid(row=i, column=1)

    def solved_message(self, solved: bool = None, message: str = None) -> None:
        for label in self.solution_labels.values():
            label.grid_forget()
            if solved is None and message is None:
                return
        if message is None:
            if solved:
                label = self.solution_labels["solved"]
            else:
                label = self.solution_labels["unsolved"]
        else:
            self.step_label.set(message)
            label = self.solution_labels["message"]
        assert label is not None
        label.grid(row=len(self.buttons), column=0, sticky="new")


class tk_Sudoku(tk.Frame):
    """Represents and displays a Sudoku in the GUI."""

    def __init__(self, parent=None, cnf={}, **kwargs):
        super().__init__(parent, cnf, **kwargs)
        self.parent = parent
        self.controller = parent
        self.children = {}
        self.sudoku: Sudoku = Sudoku()
        self.cell_dict: dict = {}
        self.new_sudoku(init=True)
        self.solver = None
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

    def __getattr__(self, item):
        """Allows us to treat this window as the actual sudoku
        when convenient."""
        if item in self.__dict__:
            return self.__dict__[item]
        else:
            return getattr(self.sudoku, item)

    def __getitem__(self, item):
        return self.sudoku[item]

    def new_sudoku(self, init=False) -> None:
        if init:
            self.sudoku = Sudoku()
            for k, v in self.sudoku.cell_dict.items():
                self.cell_dict[k] = tk_Cell(v.coordinates, parent=self, controller=self.controller)
        else:
            for key in self.cell_dict.keys():
                self.sudoku.cell_dict[key] = Cell(key)
            self.sudoku = load_puzzle()
            self.update_frames()
            self.controller.solved_message()

    def reset(self) -> None:
        self.sudoku = Sudoku()
        self.update_frames()
        self.controller.solved_message()

    def update_pms(self):
        self.update_pencil_marks()
        self.update_frames()

    def update_frames(self):
        for tk_cell in self.cell_dict.values():
            tk_cell.update_frames()

    def solve(self):
        """Solves the current sudoku."""
        self.solver = Solver(self.sudoku)
        result = self.solver.main()
        self.controller.solved_message(result)
        self.update_frames()

    def step(self):
        """Performs one logical step."""
        if self.solver is None:
            self.solver = Solver(self.sudoku)
        result = self.solver.step(message=True)
        if result is not None:
            level = result[0]
            strategy = result[1]
            message = f"Applied {level} strategy: {strategy}."
        else:
            message = "No Step Was Taken."
        self.controller.solved_message(message=message)
        self.update_frames()


class tk_Cell(tk.Frame):
    """Represents and displays Cells in the GUI."""

    def __init__(self, key: tuple[int, int], parent: tk_Sudoku = None,
                 controller: Application = None, cnf={}, **kwargs):
        super().__init__(parent, cnf, **kwargs)
        self.parent = parent
        self.controller = controller
        self.key = key
        self.frames = {}
        for F in tk_PencilMarks, tk_Digit, DigitEntry:
            name = F.__name__
            frame = F(parent=self, controller=self.controller, width=0)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.update_frames()

        self.bind("<Enter>", lambda x: self.raise_digit_entry(override=False))
        self.bind("<Leave>", lambda x: self.update_frames())
        self.bind("<Button-1>", lambda x: self.raise_digit_entry(override=True))

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

    def raise_digit_entry(self, override=False) -> None:
        if self.is_empty or override is True:
            self.show_frame("DigitEntry")

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
        self.bind("<Enter>", lambda x: self.parent.raise_digit_entry(override=self.parent.started_empty))

    def update_values(self) -> None:
        self.text.set(self.digit())

    def digit(self) -> str:
        return self.parent.digit


class DigitEntry(tk.Entry):
    """For inputting digits into the grid manually."""
    def __init__(self, parent: tk_Cell = None, controller: Application = None, **kwargs):
        super().__init__(master=parent, **kwargs)
        self.parent = parent
        self.config(font=DIGIT)
        self.controller = controller
        self.text = tk.StringVar()
        self.bind("<Key>", self.key_press)
        self.bind("<Enter>", self.raise_digit)

    def key_press(self, event) -> None:
        self.text.set(event.char)
        self.update_values()
        self.delete(0)

    def update_values(self) -> None:
        text = self.text.get()
        if text.isdigit():
            if int(text) in range(1, 10):
                self.controller.sudoku[self.parent.coordinates].fill(text)
                self.controller.sudoku.update_frames()
        self.text.set("")

    def raise_digit(self, event) -> None:
        if not self.parent.started_empty:
            self.tkraise()



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
            raise ValueError(f"File {path} does not have a supported file type. "
                             f"Please use .txt or .json.")


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
