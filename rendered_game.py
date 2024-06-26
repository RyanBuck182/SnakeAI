from game import Game
from game_handler import GameHandler
from game_renderer import GameRenderer
from game_controller import GameController
import time


class RenderedGame(Game):
    DEFAULT_SECONDS_PER_UPDATE = 0.15

    def __init__(self,
                 game_handler: GameHandler,
                 game_controller: GameController,
                 game_renderer: GameRenderer,
                 seconds_per_update: float = DEFAULT_SECONDS_PER_UPDATE):
        super().__init__(game_handler, game_controller)
        self.renderer = game_renderer
        self.seconds_per_update = seconds_per_update

    def run(self) -> int:
        last_move_time = time.time()
        while not self.handler.game_over:
            self.controller.read_input()

            progress_to_next_update = (time.time() - last_move_time) / self.seconds_per_update
            if progress_to_next_update >= 1:
                last_move_time = time.time()
                self.controller.calculate_input(self.handler)
                self.handler.update_game(self.controller.get_input())

            self.renderer.draw_game(self.handler, (progress_to_next_update if progress_to_next_update < 1 else 0))

        return self.handler.score