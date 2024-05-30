from typing import Callable


class Menu:
    def __init__(self):
        self.option_names = []
        self.option_funcs = []
        self.selection = 0

    def add_option(self, name: str, func: Callable):
        self.option_names.append(name)
        self.option_funcs.append(func)

    def select_current(self):
        self.select_option(self.selection)

    def select_option(self, selection: int):
        if len(self.option_funcs) < selection + 1:
            raise "ERROR: Cannot select option that does not exist"
        self.option_funcs[selection]()

    def selection_up(self):
        self.selection = max(self.selection - 1, 0)

    def selection_down(self):
        self.selection = min(self.selection + 1, len(self.option_funcs) - 1)