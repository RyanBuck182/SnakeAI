from typing import Callable
import pygame
from coordinate import Coordinate
from rendered_game import RenderedGame
from game_handler import GameHandler
from pygame_game_renderer import PygameGameRenderer
from pygame_game_controller import PygameGameController
from pygame_menu import PygameMenu
from selectable_menu_element import SelectableMenuElement
from optioned_menu_element import OptionedMenuElement, MenuElementOption

DEFAULT_SCREEN_DIMENSIONS = Coordinate(640, 640)
SCREEN_DIMENSION_OPTIONS = [
    MenuElementOption('320x320', Coordinate(320, 320)),
    MenuElementOption('480x480', Coordinate(480, 480)),
    MenuElementOption('640x640', Coordinate(640, 640)),
    MenuElementOption('800x800', Coordinate(800, 800)),
    MenuElementOption('960x960', Coordinate(960, 960)),
]
GRID_DIMENSION_OPTIONS = [
    MenuElementOption('8x8', Coordinate(8, 8)),
    MenuElementOption('12x12', Coordinate(12, 12)),
    MenuElementOption('16x16', Coordinate(16, 16)),
    MenuElementOption('24x24', Coordinate(24, 24)),
    MenuElementOption('32x32', Coordinate(32, 32)),
    MenuElementOption('48x48', Coordinate(48, 48)),
    MenuElementOption('64x64', Coordinate(64, 64)),
    MenuElementOption('96x96', Coordinate(96, 96)),
    MenuElementOption('128x128', Coordinate(128, 128))
]

pygame.init()
pygame.display.set_caption("Snake")
screen = pygame.display.set_mode(tuple(DEFAULT_SCREEN_DIMENSIONS))


def QUIT_GAME_FROM_UI():
    return None


def main_menu() -> Callable:
    menu = PygameMenu(screen)

    play_snake = SelectableMenuElement("Play Snake", on_select=lambda: pre_game_menu)
    watch_ai = SelectableMenuElement("Watch AI", on_select=lambda: QUIT_GAME_FROM_UI)
    quit_game = SelectableMenuElement("Quit", on_select=lambda: QUIT_GAME_FROM_UI)

    menu.add_element(play_snake)
    menu.add_element(watch_ai)
    menu.add_element(quit_game)

    return menu.load()


def pre_game_menu() -> Callable:
    menu = PygameMenu(screen)

    screen_size = OptionedMenuElement("Screen Size", SCREEN_DIMENSION_OPTIONS, on_select=menu.selection_down)
    grid_size = OptionedMenuElement("Grid Size", GRID_DIMENSION_OPTIONS, on_select=menu.selection_down)
    play = SelectableMenuElement("Play", on_select=lambda: lambda: play_manual(screen_size.get_selected_value(),
                                                                               grid_size.get_selected_value()))
    back = SelectableMenuElement("Back", on_select=lambda: main_menu)

    menu.add_element(screen_size)
    menu.add_element(grid_size)
    menu.add_element(play)
    menu.add_element(back)

    return menu.load()


def play_manual(screen_dimensions: Coordinate, grid_dimensions: Coordinate) -> Callable:
    player_start_pos = Coordinate(0, 0)
    player_start_length = 4
    handler = GameHandler(grid_dimensions, player_start_pos, player_start_length)

    global screen
    screen = pygame.display.set_mode(tuple(screen_dimensions))
    renderer = PygameGameRenderer(screen)

    controller = PygameGameController()

    game = RenderedGame(handler, controller, renderer)
    score = game.run()
    print(score)

    screen = pygame.display.set_mode(tuple(DEFAULT_SCREEN_DIMENSIONS))
    return main_menu
