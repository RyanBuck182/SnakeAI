from typing import Optional, Callable
from menu_element import MenuElement
from selectable_menu_element import SelectableMenuElement
from optioned_menu_element import OptionedMenuElement


class Menu:
    def __init__(self):
        self.elements = []
        self.selectable_elements = []
        self.selection = 0

    def add_element(self, element: MenuElement):
        total_height_percent = 0
        for v in self.elements:
            total_height_percent += v.height_percent if v.height_percent is not None else 0
        if total_height_percent + (element.height_percent if element.height_percent is not None else 0) > 1:
            raise "Total height percent of elements can not be above 1"

        self.elements.append(element)
        if isinstance(element, SelectableMenuElement):
            self.selectable_elements.append(element)

    def select_current(self) -> Optional[Callable]:
        return self.select_element(self.selection)

    def select_element(self, selection: int) -> Optional[Callable]:
        if len(self.selectable_elements) < selection + 1:
            raise "ERROR: Cannot select option that does not exist"
        return self.selectable_elements[selection].select()

    def selection_up(self):
        self.selection = max(self.selection - 1, 0)

    def selection_down(self):
        self.selection = min(self.selection + 1, len(self.selectable_elements) - 1)

    def selection_left(self):
        if isinstance(self.selectable_elements[self.selection], OptionedMenuElement):
            self.selectable_elements[self.selection].left()

    def selection_right(self):
        if isinstance(self.selectable_elements[self.selection], OptionedMenuElement):
            self.selectable_elements[self.selection].right()

    def load(self) -> Optional[Callable]:
        pass
