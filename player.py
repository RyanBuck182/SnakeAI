from direction import Direction
from coordinate import Coordinate, CoordinateF


class Player:
    def __init__(self,
                 head_pos: Coordinate,
                 segment_count: int):
        self.direction = Direction.EAST
        self.body = [Segment(self.direction, head_pos)]
        for i in range(segment_count - 1):
            self.add_segment()

    def move_forward(self):
        self.body[0].change_position(self.direction.to_coordinate())
        for i in range(1, len(self.body)):
            previous_position = self.body[i - 1].previous_position
            self.body[i].set_position(previous_position)

    def turn(self, new_direction: Direction):
        if new_direction is None:
            return

        # Can't make a 180
        if abs(int(self.direction) - int(new_direction)) == 2:
            return

        self.direction = new_direction

    def add_segment(self):
        self.body.append(Segment(self.direction,
                                 self.body[-1].position,
                                 self.body[-1].previous_position))


class Segment:
    def __init__(self,
                 player_direction: Direction,
                 position: Coordinate,
                 previous_position: Coordinate = None):
        self.position = position
        self.previous_position = position - player_direction.to_coordinate() if previous_position is None \
            else previous_position

    def change_position(self, position: Coordinate):
        self.previous_position = self.position
        self.position += position

    def set_position(self, position: Coordinate):
        self.previous_position = self.position
        self.position = position
