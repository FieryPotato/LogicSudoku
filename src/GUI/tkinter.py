from tkinter import *
from tkinter import filedialog

from src.Sudoku import Sudoku


class App(Tk):
    def __init__(self):
        super().__init__()

    def load_puzzle(self) -> Sudoku:
        path: str = filedialog.askopenfilename(
            title="Select a file", filetypes=(("JSON files", "*.json"), ("text files", "*.txt")),
        )
        with open(path, "r") as file:
            if path.endswith(".txt"):
                contents = file.read()
                return Sudoku.from_string(contents)

