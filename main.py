import pygame
from coordinate import Coordinate
from game import Game
from game_handler import GameHandler
from pygame_game_renderer import PygameGameRenderer
from pygame_game_controller import PygameGameController

pygame.init()

GRID_DIMENSIONS = Coordinate(32, 32)
PLAYER_START_POS = Coordinate(0, 0)
PLAYER_START_LENGTH = 4
handler = GameHandler(GRID_DIMENSIONS, PLAYER_START_POS, PLAYER_START_LENGTH)

SCREEN_DIMENSIONS = Coordinate(640, 640)
renderer = PygameGameRenderer(SCREEN_DIMENSIONS)

controller = PygameGameController()

SECONDS_PER_MOVE = 0.15
game = Game(handler, renderer, controller, SECONDS_PER_MOVE)
game.run()

pygame.quit()
