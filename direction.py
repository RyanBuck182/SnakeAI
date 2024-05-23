from enum import IntEnum
from coordinate import Coordinate


class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def to_coordinate(self):
        match self:
            case Direction.NORTH:
                return Coordinate(0, -1)
            case Direction.EAST:
                return Coordinate(1, 0)
            case Direction.SOUTH:
                return Coordinate(0, 1)
            case Direction.WEST:
                return Coordinate(-1, 0)
