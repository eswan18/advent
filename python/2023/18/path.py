from dataclasses import dataclass
from typing import NamedTuple

from .instruction import Instruction, Color


class Point(NamedTuple):
    x: int
    y: int


@dataclass
class Segment:
    start: Point
    end: Point
    color: Color

    def all_points(self) -> list[Point]:
        print(self)
        points = []
        if self.start.x == self.end.x:
            step = 1 if self.start.y < self.end.y else -1
            for y in range(self.start.y, self.end.y + step, step):
                points.append(Point(self.start.x, y))
        elif self.start.y == self.end.y:
            step = 1 if self.start.x < self.end.x else -1
            for x in range(self.start.x, self.end.x + step, step):
                points.append(Point(x, self.start.y))
        else:
            raise ValueError("Segment is not horizontal or vertical")
        return points


class Path:
    segments: list[Segment]

    def __init__(self):
        self.segments = []
    
    def do(self, instruction: Instruction):
        start = self.segments[-1].end if self.segments else Point(0, 0)
        end = self._calculate_end(start, instruction)
        segment = Segment(start, end, instruction.color)
        self.segments.append(segment)
    
    def _calculate_end(self, start: Point, instruction: Instruction) -> Point:
        match instruction.direction:
            case "U":
                return Point(start.x, start.y - instruction.distance)
            case "D":
                return Point(start.x, start.y + instruction.distance)
            case "L":
                return Point(start.x - instruction.distance, start.y)
            case "R":
                return Point(start.x + instruction.distance, start.y)
            case _:
                raise ValueError(f"Unknown direction: {instruction.direction}")
    
    def calculate_area(self) -> int:
        perimeter = self._calculate_perimeter()
        interior = self._calculate_interior_area()
        # About half the perimeter is actually "within" the path, so we need to add the
        # other part back in to account for the full bounded area.
        #
        # Why "about half"? Because the outer part of the perimeter (the part that we
        # didn't include in the interior) is actually longer than the inside by 2.
        # Explaining this is hard but it's easier to realize if you think about a
        # rectangle whose border is 2d squares. The edges have equal length on both
        # sides, but the corners don't: they have one quarter on the inside and 3 on the
        # outside, making each one bigger on the outside by 0.5. 4 corners * 0.5 = 2.
        #
        # So the interior includes slightly less than half the perimeter: perim / 2 - 1
        # That means we're missing the other part of the perimiter: perim / 2 + 1
        return int(interior + perimeter // 2 + 1)
     
    def _calculate_perimeter(self) -> int:
        perimeter = 0
        for segment in self.segments:
            perimeter += abs(segment.start.x - segment.end.x)
            perimeter += abs(segment.start.y - segment.end.y)
        return perimeter

    def _calculate_interior_area(self) -> int:
        if self.segments[0].start != self.segments[-1].end:
            raise ValueError("Path is not closed")
        # The "shoelace formula"
        area = 0    
        for i in range(len(self.segments) - 1):
            area += self.segments[i].start.x * self.segments[i + 1].start.y
            area -= self.segments[i + 1].start.x * self.segments[i].start.y
        return abs(area) / 2
    
    def draw(self) -> str:
        min_x = min([segment.start.x for segment in self.segments])
        min_y = min([segment.start.y for segment in self.segments])
        max_x = max([segment.start.x for segment in self.segments])
        max_y = max([segment.start.y for segment in self.segments])
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        grid = [[" "] * width for _ in range(height)]
        for segment in self.segments:
            segment_points = segment.all_points()
            for point in segment_points:
                print(point)
                grid[point.y - min_y][point.x - min_x] = "#"
        return "\n".join(["".join(row) for row in grid])