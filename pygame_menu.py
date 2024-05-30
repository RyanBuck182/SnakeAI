from math import ceil, floor
import pygame
import pygame.freetype
from coordinate import Coordinate
from menu import Menu


class PygameMenu(Menu):
    MAX_TEXT_SIZE = 70
    SELECTION_COLOR = (0, 255, 0)
    TEXT_COLOR = (255, 255, 255)
    SELECTION_INDICATOR_SIZE = 0.05
    TOP_MARGIN = 0.05
    BOTTOM_MARGIN = 0.05
    LEFT_MARGIN = 0.15

    def __init__(self, screen: pygame.Surface | pygame.SurfaceType):
        super().__init__()
        pygame.init()
        self.screen = screen
        self.screen_dimensions = Coordinate(*screen.get_size())
        self.font_path = pygame.freetype.get_default_font()

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

        locked_height_percent = 0
        unlocked_element_count = 0
        for element in self.elements:
            if element.height_percent is None:
                unlocked_element_count += 1
            else:
                locked_height_percent += element.height_percent

        unlocked_element_height_percent = (1 - locked_height_percent) / max(1, unlocked_element_count)

        for i in range(len(self.elements)):
            option_height = floor(allocated_height * unlocked_element_height_percent)
            if self.elements[i].height_percent is not None:
                option_height = floor(allocated_height * self.elements[i].height_percent)

            if i == self.selection:
                side_length = allocated_height * self.SELECTION_INDICATOR_SIZE
                pygame.draw.rect(self.screen,
                                 self.SELECTION_COLOR,
                                 pygame.Rect(
                                     floor((left_start - side_length) / 2),
                                     floor(top_start + (option_height - side_length) / 2),
                                     floor(side_length),
                                     floor(side_length)
                                 ))

            self.draw_text(self.elements[i].text,
                           Coordinate(left_start, top_start),
                           Coordinate(allocated_width, option_height))
            top_start += option_height

        pygame.display.update()
