from math import ceil, floor
from typing import Callable
import pygame
import pygame.freetype
from coordinate import Coordinate


class PygameMenu:
    MAX_TEXT_SIZE = 70
    SELECTION_COLOR = (0, 255, 0)
    TEXT_COLOR = (255, 255, 255)
    SELECTION_INDICATOR_SIZE = 0.3
    TOP_MARGIN = 0.05
    BOTTOM_MARGIN = 0.05
    LEFT_MARGIN = 0.15

    def __init__(self, screen: pygame.Surface | pygame.SurfaceType):
        pygame.init()
        self.screen = screen
        self.screen_dimensions = Coordinate(*screen.get_size())
        self.option_names = []
        self.option_funcs = []
        self.selection = 0
        self.font_path = pygame.freetype.get_default_font()

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

    def draw_text(self, text: str, start_pos: Coordinate, max_dimensions: Coordinate):
        font = pygame.freetype.SysFont(self.font_path, 1)

        def font_too_big():
            return font.get_rect(text).width > max_dimensions.x or \
                   font.get_rect(text).height > max_dimensions.y

        while not font_too_big():
            font.size += 1
        font.size -= 1
        font.size = min(self.MAX_TEXT_SIZE, floor(font.size))

        adjusted_start_position = start_pos + Coordinate(0, (max_dimensions.y - font.get_rect(text).height) / 2)

        font.render_to(self.screen,
                       tuple(adjusted_start_position),
                       text,
                       self.TEXT_COLOR)

    def draw(self):
        left_start = ceil(self.screen_dimensions.x * self.LEFT_MARGIN)
        top_start = ceil(self.screen_dimensions.y * self.TOP_MARGIN)
        bottom_end = floor(self.screen_dimensions.y * (1 - self.BOTTOM_MARGIN))

        allocated_width = self.screen_dimensions.x - left_start
        allocated_height = bottom_end - top_start
        height_per_option = floor(allocated_height / len(self.option_funcs))

        for i in range(len(self.option_names)):
            if i == self.selection:
                side_length = min(left_start * self.SELECTION_INDICATOR_SIZE, height_per_option * self.SELECTION_INDICATOR_SIZE)
                pygame.draw.rect(self.screen,
                                 self.SELECTION_COLOR,
                                 pygame.Rect(
                                     floor((left_start - side_length) / 2),
                                     floor(top_start + (height_per_option - side_length) / 2),
                                     floor(side_length),
                                     floor(side_length)
                                 ))

            self.draw_text(self.option_names[i],
                           Coordinate(left_start, top_start),
                           Coordinate(allocated_width, height_per_option))
            top_start += height_per_option

        pygame.display.update()
