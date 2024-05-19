from enum import IntEnum
from collections import deque
from coordinate import Coordinate, CoordinateF
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
                 grid_dimensions: Coordinate,
                 square_dimensions: Coordinate,
                 head_pos: Coordinate,
                 segment_count: int):
        self.grid_dimensions = grid_dimensions
        self.square_dimensions = square_dimensions
        self.body = [Segment(self.square_dimensions, head_pos)]
        for i in range(segment_count - 1):
            self.add_segment()
        self.corner_covers = []
        self.direction = Direction.EAST
        self.queued_turns = deque()

    def draw(self, screen: pygame.Surface | pygame.SurfaceType):
        for segment in self.body[1:]:
            pygame.draw.rect(screen, self.SEGMENT_COLOR, segment)
        for cover in self.corner_covers:
            pygame.draw.rect(screen, self.SEGMENT_COLOR, Segment(self.square_dimensions, cover))
        pygame.draw.rect(screen, self.HEAD_COLOR, self.body[0])

    def update_position(self, move_progress: float):
        for i in range(len(self.body)):
            self.body[i].update_drawn_position(move_progress)

    def move_forward(self):
        change = Coordinate(0, 0)
        match self.direction:
            case Direction.NORTH:
                change = Coordinate(0, -1)
            case Direction.EAST:
                change = Coordinate(1, 0)
            case Direction.SOUTH:
                change = Coordinate(0, 1)
            case Direction.WEST:
                change = Coordinate(-1, 0)

        self.corner_covers.clear()
        self.body[0].change_position(change)
        for i in range(1, len(self.body)):
            previous_position = self.body[i - 1].previous_position
            self.body[i].set_position(previous_position)

            # If move is a turn, cover the corners
            previous_change = self.body[i - 1].position - self.body[i - 1].previous_position
            current_change = self.body[i].position - self.body[i].previous_position
            if current_change != previous_change:
                self.corner_covers.append(self.body[i].position)

    def is_colliding(self) -> bool:
        if (self.body[0].position.x < 0 or
                self.body[0].position.y < 0 or
                self.body[0].position.x >= self.grid_dimensions.x or
                self.body[0].position.y >= self.grid_dimensions.y):
            return True

        for segment in self.body[1:]:
            if segment.position == self.body[0].position:
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
        self.body.append(Segment(self.square_dimensions,
                                 self.body[-1].position,
                                 self.body[-1].previous_position))


class Segment:
    def __init__(self,
                 square_dimensions: Coordinate,
                 position: Coordinate,
                 previous_position: Coordinate = None):
        self.square_dimensions = square_dimensions
        self.position = position
        self.previous_position = position - Coordinate(1, 0) if previous_position is None else previous_position
        self.rect = pygame.Rect(*(position * square_dimensions), square_dimensions.x, square_dimensions.y)

    def change_position(self, position: Coordinate):
        self.previous_position = self.position
        self.position += position

    def set_position(self, position: Coordinate):
        self.previous_position = self.position
        self.position = position

    def update_drawn_position(self, move_progress: float):
        move_percentage = (self.position - self.previous_position).to_float().scale(move_progress)
        new_position = ((self.previous_position * self.square_dimensions) +
                        (move_percentage * self.square_dimensions.to_float()).floor())
        self.rect.topleft = tuple(new_position)
