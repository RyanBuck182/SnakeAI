class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(self.x * other.x, self.y * other.y)

    def __floordiv__(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(self.x // other.x, self.y // other.y)

    def __eq__(self, other: 'Coordinate') -> bool:
        return self.x == other.x and self.y == other.y

    def __iter__(self):
        yield self.x
        yield self.y

    def scale(self, scale: int) -> 'Coordinate':
        return Coordinate(self.x * scale, self.y * scale)

    def to_float(self) -> 'CoordinateF':
        return CoordinateF(self.x, self.y)


class CoordinateF:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: 'CoordinateF') -> 'CoordinateF':
        return CoordinateF(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'CoordinateF') -> 'CoordinateF':
        return CoordinateF(self.x - other.x, self.y - other.y)

    def __mul__(self, other: 'CoordinateF') -> 'CoordinateF':
        return CoordinateF(self.x * other.x, self.y * other.y)

    def __truediv__(self, other: 'CoordinateF') -> 'CoordinateF':
        return CoordinateF(self.x / other.x, self.y / other.y)

    def __eq__(self, other: 'CoordinateF') -> bool:
        return self.x == other.x and self.y == other.y

    def __iter__(self):
        yield self.x
        yield self.y

    def scale(self, scale: float) -> 'CoordinateF':
        return CoordinateF(self.x * scale, self.y * scale)

    def floor(self) -> 'Coordinate':
        return Coordinate(int(self.x), int(self.y))