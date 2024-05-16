import pygame
import random
from player import Player


class Fruit:
    COLOR = (255, 0, 0)

    def __init__(self,
                 grid_width: int,
                 grid_height: int,
                 square_width: int,
                 square_height: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.square_width = square_width
        self.square_height = square_height
        self.grid_position = (0, 0)
        self.rect = pygame.Rect(0, 0, square_width, square_height)

    def draw(self, screen: pygame.Surface | pygame.SurfaceType):
        pygame.draw.rect(screen, self.COLOR, self.rect)

    # Should have something that can check if a position is occupied, this shouldn't check the player itself
    def randomize_position(self, player: Player):
        if len(player.body) < 0.85 * self.grid_width * self.grid_height:
            new_position = (0, 0)
            valid_position = False
            while not valid_position:
                valid_position = True
                new_position = (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))
                for segment in player.body:
                    if segment.grid_position == new_position:
                        valid_position = False
                        break
            self.grid_position = new_position
        elif len(player.body) >= self.grid_width * self.grid_height:
            self.grid_position = (-1, -1)
        else:
            valid_positions = [(i, j) for j in range(self.grid_height) for i in range(self.grid_width)]

            for segment in player.body:
                del valid_positions[segment.grid_position[0] * self.grid_height + segment.grid_position[1]]

            self.grid_position = random.choice(valid_positions)

        self.rect.topleft = (self.grid_position[0] * self.square_width, self.grid_position[1] * self.square_height)
