import json
from tkinter import *
from tkinter import filedialog

from src.Sudoku import Sudoku


class App(Tk):
    def __init__(self):
        super().__init__()
        self.puzzle = None
        self.cell_dict = {
            Widget
        }


def load_puzzle() -> Sudoku:
    path: str = filedialog.askopenfilename(
        title="Select a file", filetypes=(("JSON files", "*.json"), ("text files", "*.txt")),
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
