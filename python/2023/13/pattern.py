from dataclasses import dataclass
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


@dataclass
class Pattern:
    rocks: list[Point]

    @classmethod
    def build_from_str(cls, input: str) -> "Pattern":
        rocks = []
        for y, line in enumerate(input.splitlines()):
            for x, char in enumerate(line):
                if char == "#":
                    rocks.append(Point(x, y))
        return cls(rocks)
    

    def find_horizontal_reflection(self) -> int | None:
        # Where is the line over which this pattern is symmetrical?
        max_x = max(rock.x for rock in self.rocks)
        max_y = max(rock.y for rock in self.rocks)
        for x_line in range(0, max_x):
            # The line actually runs between two points.
            x_line = x_line + 0.5
            # Start at this point and work to the right.
            x = x_line + 0.5
            reflected_x = x_line - 0.5
            all_match = True
            while x <= max_x and reflected_x >= 0:
                for y in range(0, max_y + 1):
                    is_rock = Point(x, y) in self.rocks
                    is_reflected_rock = Point(reflected_x, y) in self.rocks
                    if is_rock != is_reflected_rock:
                        all_match = False
                        break
                x += 1
                reflected_x -= 1
            if all_match:
                return int(x_line - 0.5)
        return None
    
    def find_vertical_reflection(self) -> int | None:
        # Where is the line over which this pattern is symmetrical?
        max_x = max(rock.x for rock in self.rocks)
        max_y = max(rock.y for rock in self.rocks)
        for y_line in range(0, max_y):
            # The line actually runs between two points.
            y_line = y_line + 0.5
            # Start at this point and work down.
            y = y_line + 0.5
            reflected_y = y_line - 0.5
            all_match = True
            while y <= max_y and reflected_y >= 0:
                for x in range(0, max_x + 1):
                    is_rock = Point(x, y) in self.rocks
                    is_reflected_rock = Point(x, reflected_y) in self.rocks
                    if is_rock != is_reflected_rock:
                        all_match = False
                        break
                y += 1
                reflected_y -= 1
            if all_match:
                return int(y_line - 0.5)
        return None
    
    def find_reflect_score(self) -> int:
        vert_score = self.find_vertical_reflection()
        if vert_score is not None:
            return (vert_score + 1) * 100
        horiz_score = self.find_horizontal_reflection()
        if horiz_score is not None:
            return horiz_score + 1
        raise RuntimeError("no symmetry")
    
    def __str__(self) -> str:
        max_x = max(rock.x for rock in self.rocks)
        max_y = max(rock.y for rock in self.rocks)
        lines = []
        for y in range(0, max_y + 1):
            line = []
            for x in range(0, max_x + 1):
                if Point(x, y) in self.rocks:
                    line.append("#")
                else:
                    line.append(".")
            lines.append("".join(line))
        return "\n".join(lines)