import pygame
import time
from fruit import Fruit
from player import Player, Direction

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
GRID_WIDTH = 32
GRID_HEIGHT = 32
SQUARE_WIDTH = int(SCREEN_WIDTH / GRID_WIDTH)
SQUARE_HEIGHT = int(SCREEN_HEIGHT / GRID_HEIGHT)
SCREEN_BACKGROUND_COLOR = (0, 0, 0)
SECONDS_PER_MOVE = 0.1
PLAYER_BODY_SEGMENTS = 4

pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
player = Player(GRID_WIDTH,
                GRID_HEIGHT,
                SQUARE_WIDTH,
                SQUARE_HEIGHT,
                (3, 0),
                PLAYER_BODY_SEGMENTS)
fruit = Fruit(GRID_WIDTH,
              GRID_HEIGHT,
              SQUARE_WIDTH,
              SQUARE_HEIGHT)
fruit.randomize_position(player)

last_move_time = time.time()
run_game = True
while run_game:
    screen.fill(SCREEN_BACKGROUND_COLOR)
    player.draw(screen)
    fruit.draw(screen)

    move_progress = (time.time() - last_move_time) / SECONDS_PER_MOVE
    if move_progress >= 1:
        last_move_time = time.time()
        player.turn()
        player.move_forward()
        if player.is_colliding():
            run_game = False
        if player.body[0].grid_position == fruit.grid_position:
            player.add_segment()
            fruit.randomize_position(player)
    else:
        player.update_position(move_progress)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w | pygame.K_UP:
                    player.queue_turn(Direction.NORTH)
                case pygame.K_d | pygame.K_RIGHT:
                    player.queue_turn(Direction.EAST)
                case pygame.K_s | pygame.K_DOWN:
                    player.queue_turn(Direction.SOUTH)
                case pygame.K_a | pygame.K_LEFT:
                    player.queue_turn(Direction.WEST)

    pygame.display.update()

pygame.quit()
