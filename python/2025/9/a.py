from itertools import combinations
from typing import Self

from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        str_x, str_y = s.strip().split(',')
        return cls(x=int(str_x), y=int(str_y))


def rectangle_area(a: Point, b: Point) -> int:
    height = abs(a.y - b.y) + 1
    width = abs(a.x - b.x) + 1
    return width * height
    

def a(input: str) -> str:
    points = [Point.from_str(line) for line in input.splitlines()]

    largest_area = -1
    for a, b in combinations(points, 2):
        area = rectangle_area(a, b)
        if area > largest_area:
            largest_area = area
    
    return str(largest_area)