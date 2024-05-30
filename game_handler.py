from coordinate import Coordinate
from input import Input
from player import Player
from fruit import Fruit
import random


class GameHandler:
    DEFAULT_PLAYER_START_POS = Coordinate(0, 0)
    DEFAULT_PLAYER_START_LENGTH = 4

    def __init__(self,
                 grid_dimensions: Coordinate,
                 player_start_pos: Coordinate = DEFAULT_PLAYER_START_POS,
                 player_start_length: int = DEFAULT_PLAYER_START_LENGTH):
        self.grid_dimensions = grid_dimensions
        self.player = Player(player_start_pos, player_start_length)
        self.fruit = Fruit()
        self.randomize_fruit_position()
        self.score = 0
        self.game_over = False

    def update_game(self, player_input: Input):
        # if input includes quit, then set game_over to true
        if player_input.quit_game:
            self.game_over = True

        self.player.turn(player_input.turn_direction)
        self.player.move_forward()
        if self.is_player_colliding():
            self.game_over = True
        elif self.is_player_eating_fruit():
            self.score += 1
            self.player.add_segment()
            self.randomize_fruit_position()

    def is_player_colliding(self) -> bool:
        if (self.player.body[0].position.x < 0 or
                self.player.body[0].position.y < 0 or
                self.player.body[0].position.x >= self.grid_dimensions.x or
                self.player.body[0].position.y >= self.grid_dimensions.y):
            return True

        for segment in self.player.body[1:]:
            if segment.position == self.player.body[0].position:
                return True

        return False

    def is_player_eating_fruit(self) -> bool:
        if self.player.body[0].position == self.fruit.position:
            return True
        return False

    def randomize_fruit_position(self):
        if len(self.player.body) < 0.85 * self.grid_dimensions.x * self.grid_dimensions.y:
            new_position = Coordinate(0, 0)
            valid_position = False
            while not valid_position:
                valid_position = True
                new_position = Coordinate(random.randint(0, self.grid_dimensions.x - 1),
                                          random.randint(0, self.grid_dimensions.y - 1))
                for segment in self.player.body:
                    if segment.position == new_position:
                        valid_position = False
                        break
            self.fruit.position = new_position
        elif len(self.player.body) >= self.grid_dimensions.x * self.grid_dimensions.y:
            # HANDLE WIN!!!!!!!!!!!!
            self.fruit.position = Coordinate(-1, -1)
        else:
            valid_positions = [Coordinate(i, j)
                               for j in range(self.grid_dimensions.y)
                               for i in range(self.grid_dimensions.x)]

            for segment in self.player.body:
                del valid_positions[segment.position.x * self.grid_dimensions.y + segment.position.y]

            self.fruit.position = random.choice(valid_positions)
