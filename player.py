from enum import IntEnum
from collections import deque
import pygame


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Player:
    TURN_QUEUE_MAX = 2
    HEAD_COLOR = (0, 255, 0)
    SEGMENT_COLOR = (0, 255, 0)

    def __init__(self,
                 grid_width: int,
                 grid_height: int,
                 square_width: int,
                 square_height: int,
                 head_grid_position: tuple[int, int],
                 segment_count: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.square_width = square_width
        self.square_height = square_height
        self.body = [Segment(square_width, square_height, head_grid_position)]
        for i in range(segment_count - 1):
            self.add_segment()
        self.corner_covers = []
        self.direction = Direction.EAST
        self.queued_turns = deque()

    def draw(self, screen: pygame.Surface | pygame.SurfaceType):
        for segment in self.body[1:]:
            pygame.draw.rect(screen, self.SEGMENT_COLOR, segment)
        for cover in self.corner_covers:
            pygame.draw.rect(screen, self.SEGMENT_COLOR, Segment(self.square_width, self.square_height, cover))
        pygame.draw.rect(screen, self.HEAD_COLOR, self.body[0])

    def update_position(self, move_progress: float):
        for i in range(len(self.body)):
            self.body[i].update_drawn_position(move_progress)

    def move_forward(self):
        change = (0, 0)
        match self.direction:
            case Direction.NORTH:
                change = (0, -1)
            case Direction.EAST:
                change = (1, 0)
            case Direction.SOUTH:
                change = (0, 1)
            case Direction.WEST:
                change = (-1, 0)

        self.corner_covers.clear()
        self.body[0].change_position(change)
        for i in range(1, len(self.body)):
            previous_position = self.body[i - 1].previous_position
            self.body[i].set_position(previous_position)
            previous_change = tuple(self.body[i - 1].grid_position[j] -
                                    self.body[i - 1].previous_position[j]
                                    for j in range(2))
            current_change = tuple(self.body[i].grid_position[j] -
                                   self.body[i].previous_position[j]
                                   for j in range(2))
            if current_change != previous_change:
                self.corner_covers.append(self.body[i].grid_position)

    def is_colliding(self) -> bool:
        if (self.body[0].grid_position[0] < 0 or
                self.body[0].grid_position[1] < 0 or
                self.body[0].grid_position[0] >= self.grid_width or
                self.body[0].grid_position[1] >= self.grid_height):
            return True

        for segment in self.body[1:]:
            if all(segment.grid_position[i] == self.body[0].grid_position[i] for i in range(2)):
                return True

        return False

    def turn(self):
        if not self.queued_turns:
            return

        # Can't make a 180
        if abs(int(self.direction) - int(self.queued_turns[0])) == 2:
            self.queued_turns.popleft()
            return

        self.direction = self.queued_turns.popleft()

    def queue_turn(self, direction: Direction):
        # Add to queue if queue is empty OR
        # last queued direction is not the same as new direction AND
        # queue is below the maximum allowed queued turns
        if (not self.queued_turns or
                (self.queued_turns[-1] != direction and
                 len(self.queued_turns) < self.TURN_QUEUE_MAX)):
            self.queued_turns.append(direction)

    def add_segment(self):
        self.body.append(Segment(self.square_width, self.square_height, self.body[-1].previous_position))


class Segment:
    def __init__(self, square_width: int, square_height: int, grid_position: tuple[int, int]):
        self.square_width = square_width
        self.square_height = square_height
        self.grid_position = grid_position
        self.previous_position = (grid_position[0] - 1, grid_position[1])
        self.rect = pygame.Rect(square_width * grid_position[0],
                                square_height * grid_position[1],
                                square_width,
                                square_height)

    def change_position(self, grid_position: tuple[int, int]):
        self.previous_position = self.grid_position
        self.grid_position = tuple(self.grid_position[i] + grid_position[i] for i in range(2))

    def set_position(self, grid_position: tuple[int, int]):
        self.previous_position = self.grid_position
        self.grid_position = grid_position

    def update_drawn_position(self, move_progress: float):
        move_change_percentage = tuple(
            (self.grid_position[i] - self.previous_position[i]) * move_progress
            for i in range(2))
        self.rect.topleft = (int((self.previous_position[0] + move_change_percentage[0]) * self.square_width),
                             int((self.previous_position[1] + move_change_percentage[1]) * self.square_height))
