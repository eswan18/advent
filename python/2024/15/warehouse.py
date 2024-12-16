import time
from typing import Self, Literal
from dataclasses import dataclass

Move = Literal["^", "<", ">", "v"]


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y)

    def __mul__(self, multiplier: int) -> Self:
        return self.__class__(self.x * multiplier, self.y * multiplier)

    def coordinate(self) -> int:
        return 100 * self.y + self.x

    def shift_for_big_map(self) -> Self:
        return Position(self.x * 2, self.y)


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


@dataclass
class BigWarehouse:
    robot: Position
    wide_boxes: set[Position]
    walls: set[Position]
    width: int
    height: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        warehouse = Warehouse.from_str(s)
        # Fix each element, one at a time.
        robot = warehouse.robot.shift_for_big_map()
        walls = set()
        for wall in warehouse.walls:
            new_wall_pos = wall.shift_for_big_map()
            second_wall_pos = Position(new_wall_pos.x + 1, new_wall_pos.y)
            walls.add(new_wall_pos)
            walls.add(second_wall_pos)
        wide_boxes = set(box.shift_for_big_map() for box in warehouse.boxes)
        width = warehouse.width * 2
        height = warehouse.height
        return cls(
            robot=robot,
            wide_boxes=wide_boxes,
            walls=walls,
            width=width,
            height=height,
        )

    def __str__(self) -> str:
        s = ""
        for y in range(self.height):
            for x in range(self.width):
                s += self[Position(x, y)]
            s += "\n"
        return s

    def __getitem__(self, key: Position) -> str:
        """Get the "thing" at self[x, y]."""
        if not isinstance(key, Position):
            raise TypeError("Can only look up items using Position")
        if key in self.walls:
            return "#"
        elif key in self.wide_boxes:
            return "["
        elif Position(key.x - 1, key.y) in self.wide_boxes:
            return "]"
        elif key == self.robot:
            return "@"
        else:
            return "."

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
        to_shift: list[set[Position]] = []
        to_shift.append({self.robot})
        while True:
            # Get the last row of things that are shifting to see what it'll run into.
            top_line_shifting = to_shift[-1]
            spots_to_check: set[Position] = set()
            for pos in top_line_shifting:
                if self[pos] == "@":
                    spots_to_check.add(pos + direction)
                if self[pos] == "[":
                    match move:
                        case "^" | "v":
                            # We need to check above/below both sides of this box.
                            spots_to_check.add(pos + direction)
                            spots_to_check.add(Position(pos.x + 1, pos.y) + direction)
                        case ">":
                            # We need to move over 2 to hop over the right side of this current box.
                            spots_to_check.add(pos + direction * 2)
                        case "<":
                            spots_to_check.add(pos + direction)
            next_to_shift = set()
            stuck = False
            for spot in spots_to_check:
                thing = self[spot]
                if thing == "#":
                    # We're stuck!
                    stuck = True
                    break
                if thing == "[":
                    # Left half of a box – add it to our to_shift
                    next_to_shift.add(spot)
                if thing == "]":
                    # Right half of a box – add it to our to_shift
                    spot = Position(spot.x - 1, spot.y)
                    next_to_shift.add(spot)
            if stuck:
                break
            if len(next_to_shift) == 0:
                break
            # Record the newest rocks we need to shift and loop again.
            to_shift.append(next_to_shift)
        if not stuck:
            # Remove all the boxes we're shifting and re-add them, but shifted.
            all_to_shift = [pos for pos_set in to_shift for pos in pos_set]
            all_to_shift.remove(self.robot)
            for pos in all_to_shift:
                self.wide_boxes.remove(pos)
            for pos in all_to_shift:
                self.wide_boxes.add(pos + direction)
            # Shift the robot
            self.robot = self.robot + direction

    def sum_of_box_coords(self) -> int:
        running_sum = 0
        for box in self.wide_boxes:
            running_sum += box.coordinate()
        return running_sum
