from typing import Callable
from menu_element import MenuElement


class SelectableMenuElement(MenuElement):
    def __init__(self,
                 text: str,
                 height_percent: float = None,
                 *,
                 on_select: Callable = lambda: None):
        super().__init__(text, height_percent)
        self.select = on_select
