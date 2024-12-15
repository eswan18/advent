from typing import Self, Literal
from dataclasses import dataclass

Move = Literal["^", "<", ">", "v"]


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y)
    
    def coordinate(self) -> int:
        return 100 * self.y + self.x


@dataclass
class Warehouse:
    robot: Position
    boxes: set[Position]
    walls: set[Position]
    width: int
    height: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        # Warehouse diagrams look like this:
        # ##########
        # #..O..O.O#
        # #......O.#
        # #.OO..O.O#
        # #..O@..O.#
        # #O#..O...#
        # #O..O..O.#
        # #.OO.O.OO#
        # #....O...#
        # ##########
        boxes = set()
        walls = set()
        robot = Position(-1, -1)
        lines = s.splitlines()
        height = len(lines)
        width = len(lines[0])
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == "#":
                    walls.add(Position(x, y))
                elif c == "O":
                    boxes.add(Position(x, y))
                elif c == "@":
                    robot = Position(x, y)
        return cls(robot=robot, boxes=boxes, walls=walls, width=width, height=height)

    def __getitem__(self, key: Position) -> str:
        """Get the "thing" at self[x, y]."""
        if not isinstance(key, Position):
            raise TypeError("Can only look up items using Position")
        if key in self.walls:
            return "#"
        elif key in self.boxes:
            return "O"
        elif key == self.robot:
            return "@"
        else:
            return "."

    def __str__(self) -> str:
        s = ""
        for y in range(self.height):
            for x in range(self.width):
                s += self[Position(x, y)]
            s += "\n"
        return s

    def make_move(self, move: Move):
        direction = None
        match move:
            case "^":
                direction = Position(0, -1)
            case "v":
                direction = Position(0, 1)
            case ">":
                direction = Position(1, 0)
            case "<":
                direction = Position(-1, 0)
            case m:
                raise ValueError(f'unexpected token "{m}"')
        to_shift = set()
        pos = self.robot + direction
        found_gap = False
        while True:
            at_position = self[pos]
            # Keep looping until we hit a wall or a gap.
            if at_position == "#":
                break
            if at_position == ".":
                found_gap = True
                break
            if at_position == "O":
                to_shift.add(pos)
            pos += direction
        if found_gap:
            # Shift the robot
            self.robot = self.robot + direction
            # Remove all the boxes we're shifting and re-add them, but shifted.
            for pos in to_shift:
                self.boxes.remove(pos)
            for pos in to_shift:
                self.boxes.add(pos + direction)

    def sum_of_box_coords(self) -> int:
        running_sum = 0
        for box in self.boxes:
            running_sum += box.coordinate()
        return running_sum