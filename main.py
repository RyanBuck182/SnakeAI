import os
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

def main_menu():
    menu = PygameMenu(screen)
    menu.add_element(SelectableMenuElement("Play Snake", on_select=pre_game_menu))
    menu.add_element(SelectableMenuElement("Train AI", on_select=lambda: None))
    menu.add_element(SelectableMenuElement("Quit", on_select=pygame.quit))

    selection = None
    while selection is None:
        screen.fill((0, 0, 0))
        menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                selection = 2
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w | pygame.K_UP:
                        menu.selection_up()
                    case pygame.K_s | pygame.K_DOWN:
                        menu.selection_down()
                    case pygame.K_RETURN:
                        selection = menu.selection

    menu.select_element(selection)

def pre_game_menu():
    menu = PygameMenu(screen)
    menu.add_element(OptionedMenuElement("Screen Size", SCREEN_DIMENSION_OPTIONS, on_select=menu.selection_down))
    menu.add_element(OptionedMenuElement("Grid Size", GRID_DIMENSION_OPTIONS, on_select=menu.selection_down))

    def select_play():
        play_manual(menu.selectable_elements[0].get_selected_value(), menu.selectable_elements[1].get_selected_value())
    menu.add_element(SelectableMenuElement("Play", on_select=select_play))
    menu.add_element(SelectableMenuElement("Back", on_select=main_menu))

    selection_complete = False
    while not selection_complete:
        screen.fill((0, 0, 0))
        menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                selection_complete = True
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w | pygame.K_UP:
                        menu.selection_up()
                    case pygame.K_s | pygame.K_DOWN:
                        menu.selection_down()
                    case pygame.K_d | pygame.K_RIGHT:
                        menu.selection_right()
                    case pygame.K_a | pygame.K_LEFT:
                        menu.selection_left()
                    case pygame.K_RETURN:
                        menu.select_current()
                        if menu.selection in [3, 4]:
                            selection_complete = True

def play_manual(screen_dimensions: Coordinate, grid_dimensions: Coordinate):
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
    main_menu()


if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

    main_menu()
