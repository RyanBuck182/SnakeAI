from direction import Direction


class Input:
    def __init__(self, turn_direction: Direction | None, quit_game: bool = False):
        self.quit_game = quit_game
        self.turn_direction = turn_direction
