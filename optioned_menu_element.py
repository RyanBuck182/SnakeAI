from typing import Callable, Any
from selectable_menu_element import SelectableMenuElement


class OptionedMenuElement(SelectableMenuElement):
    def __init__(self,
                 label: str,
                 options: list,
                 height_percent: float = None,
                 *,
                 on_select: Callable = lambda: None,
                 selected_option: int = 0):
        super().__init__(label + ':  <' + options[selected_option].name + '>',
                         height_percent,
                         on_select=on_select)
        self.label = label
        self.options = options
        self.selected_option = selected_option

    def format_text(self):
        self.text = self.label + ':  <' + self.options[self.selected_option].name + '>'

    def left(self):
        self.selected_option = max(self.selected_option - 1, 0)
        self.format_text()

    def right(self):
        self.selected_option = min(self.selected_option + 1, len(self.options) - 1)
        self.format_text()

    def get_selected_value(self):
        return self.options[self.selected_option].value


class MenuElementOption:
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value
