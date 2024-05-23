from collections import deque
from game_controller import GameController
from input import Input
from direction import Direction
import pygame


class PygameGameController(GameController):
    MAX_QUEUED_TURNS = 2

    def __init__(self):
        pygame.init()
        self.quit_game = False
        self.queued_turns = deque()

    def get_input(self) -> Input:
        if len(self.queued_turns) == 0:
            return Input(None, self.quit_game)
        else:
            return Input(self.queued_turns.popleft(), self.quit_game)

    def read_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game = True
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w | pygame.K_UP:
                        self.queue_turn(Direction.NORTH)
                    case pygame.K_d | pygame.K_RIGHT:
                        self.queue_turn(Direction.EAST)
                    case pygame.K_s | pygame.K_DOWN:
                        self.queue_turn(Direction.SOUTH)
                    case pygame.K_a | pygame.K_LEFT:
                        self.queue_turn(Direction.WEST)

    def queue_turn(self, direction: Direction):
        # Add to queue if queue is empty OR
        # last queued direction is not the same as new direction AND
        # queue is below the maximum allowed queued turns
        if (not self.queued_turns or
                (self.queued_turns[-1] != direction and
                 len(self.queued_turns) < self.MAX_QUEUED_TURNS)):
            self.queued_turns.append(direction)
