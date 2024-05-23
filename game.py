from game_handler import GameHandler
from game_renderer import GameRenderer
from game_controller import GameController
import time


class Game:
    def __init__(self,
                 game_handler: GameHandler,
                 game_renderer: GameRenderer,
                 game_controller: GameController,
                 seconds_per_update: float):
        self.handler = game_handler
        self.renderer = game_renderer
        self.controller = game_controller
        self.seconds_per_update = seconds_per_update

    def run(self):
        last_move_time = time.time()
        while not self.handler.game_over:
            self.controller.read_input()

            progress_to_next_update = (time.time() - last_move_time) / self.seconds_per_update
            if progress_to_next_update >= 1:
                last_move_time = time.time()
                self.handler.update_game(self.controller.get_input())

            self.renderer.draw_game(self.handler, (progress_to_next_update if progress_to_next_update < 1 else 0))
