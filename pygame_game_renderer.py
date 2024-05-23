import pygame
from coordinate import Coordinate
from game_renderer import GameRenderer
from game_handler import GameHandler
from player import Player
from fruit import Fruit


class PygameGameRenderer(GameRenderer):
    DEFAULT_BACKGROUND_COLOR = (0, 0, 0)
    DEFAULT_PLAYER_COLOR = (0, 255, 0)
    DEFAULT_FRUIT_COLOR = (255, 0, 0)

    def __init__(self,
                 screen_dimensions: Coordinate,
                 background_color: tuple[int, int, int] = DEFAULT_BACKGROUND_COLOR,
                 player_color: tuple[int, int, int] = DEFAULT_PLAYER_COLOR,
                 fruit_color: tuple[int, int, int] = DEFAULT_FRUIT_COLOR):
        self.screen_dimensions = screen_dimensions
        self.background_color = background_color
        self.player_color = player_color
        self.fruit_color = fruit_color

        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode(tuple(screen_dimensions))

    def draw_game(self, game_handler: GameHandler, move_progress: float):
        square_dimensions = self.screen_dimensions // game_handler.grid_dimensions

        self.draw_background()
        self.draw_player(square_dimensions, move_progress, game_handler.player)
        self.draw_fruit(square_dimensions, game_handler.fruit)
        pygame.display.update()

    def draw_background(self):
        self.screen.fill(self.background_color)

    def draw_player(self, square_dimensions: Coordinate, move_progress: float, player: Player):
        for segment in player.body:
            move_percentage = (segment.position - segment.previous_position).to_float().scale(move_progress)
            drawn_position = ((segment.previous_position * square_dimensions) +
                              (move_percentage * square_dimensions.to_float()).floor())
            pygame.draw.rect(self.screen,
                             self.player_color,
                             pygame.Rect(*drawn_position, *square_dimensions))

        for i in range(1, len(player.body)):
            previous_change = player.body[i - 1].position - player.body[i - 1].previous_position
            current_change = player.body[i].position - player.body[i].previous_position
            if current_change != previous_change:
                pygame.draw.rect(self.screen,
                                 self.player_color,
                                 pygame.Rect(*(player.body[i].position * square_dimensions), *square_dimensions))

    def draw_fruit(self, square_dimensions: Coordinate, fruit: Fruit):
        pygame.draw.rect(self.screen,
                         self.fruit_color,
                         pygame.Rect(*(fruit.position * square_dimensions), *square_dimensions))
