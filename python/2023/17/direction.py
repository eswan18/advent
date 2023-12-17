from enum import StrEnum


class Direction(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)

    def opposite(self) -> 'Direction':
        if self is Direction.UP:
            return Direction.DOWN
        if self is Direction.DOWN:
            return Direction.UP
        if self is Direction.LEFT:
            return Direction.RIGHT
        if self is Direction.RIGHT:
            return Direction.LEFT