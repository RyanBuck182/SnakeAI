import pygame
import random
from coordinate import Coordinate
from player import Player


class Fruit:
    COLOR = (255, 0, 0)

    def __init__(self,
                 grid_dimensions: Coordinate,
                 square_dimensions: Coordinate):
        self.grid_dimensions = grid_dimensions
        self.square_dimensions = square_dimensions
        self.position = Coordinate(0, 0)
        self.rect = pygame.Rect(0, 0, *square_dimensions)

    def draw(self, screen: pygame.Surface | pygame.SurfaceType):
        pygame.draw.rect(screen, self.COLOR, self.rect)

    # Should have something that can check if a position is occupied, this shouldn't check the player itself
    def randomize_position(self, player: Player):
        if len(player.body) < 0.85 * self.grid_dimensions.x * self.grid_dimensions.y:
            new_position = Coordinate(0, 0)
            valid_position = False
            while not valid_position:
                valid_position = True
                new_position = Coordinate(random.randint(0, self.grid_dimensions.x - 1),
                                          random.randint(0, self.grid_dimensions.y - 1))
                for segment in player.body:
                    if segment.position == new_position:
                        valid_position = False
                        break
            self.position = new_position
        elif len(player.body) >= self.grid_dimensions.x * self.grid_dimensions.y:
            # HANDLE WIN!!!!!!!!!!!!
            self.position = Coordinate(-1, -1)
        else:
            valid_positions = [Coordinate(i, j)
                               for j in range(self.square_dimensions.y)
                               for i in range(self.square_dimensions.x)]

            for segment in player.body:
                del valid_positions[segment.position.x * self.grid_dimensions.y + segment.position.y]

            self.position = random.choice(valid_positions)

        self.rect.topleft = tuple(self.position * self.square_dimensions)
