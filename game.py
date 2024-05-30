from game_handler import GameHandler
from game_controller import GameController


class Game:
    def __init__(self,
                 game_handler: GameHandler,
                 game_controller: GameController):
        self.handler = game_handler
        self.controller = game_controller

    def run(self):
        while not self.handler.game_over:
            self.controller.read_input()
            self.controller.calculate_input(self.handler)
            self.handler.update_game(self.controller.get_input())
