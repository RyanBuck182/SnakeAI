import pygame
from coordinate import Coordinate
from rendered_game import RenderedGame
from game_handler import GameHandler
from pygame_game_renderer import PygameGameRenderer
from pygame_game_controller import PygameGameController
from pygame_menu import PygameMenu

SCREEN_DIMENSIONS = Coordinate(640, 640)

pygame.init()
pygame.display.set_caption("Snake")
SCREEN = pygame.display.set_mode(tuple(SCREEN_DIMENSIONS))


def main_menu():
    menu = PygameMenu(SCREEN)
    menu.add_option("Play Snake", play_manual)
    menu.add_option("Train AI", None)
    menu.add_option("Quit", pygame.quit)

    selection = None
    while selection is None:
        SCREEN.fill((0, 0, 0))
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

    menu.select_option(selection)


def play_manual():
    grid_dimensions = Coordinate(32, 32)
    player_start_pos = Coordinate(0, 0)
    player_start_length = 4
    handler = GameHandler(grid_dimensions, player_start_pos, player_start_length)

    renderer = PygameGameRenderer(SCREEN)

    controller = PygameGameController()

    game = RenderedGame(handler, controller, renderer)
    game.run()

    main_menu()


if __name__ == '__main__':
    main_menu()
