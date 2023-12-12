from dataclasses import dataclass
from typing import NamedTuple

class Point(NamedTuple):
    x: int
    y: int

@dataclass
class Universe:
    galaxies: list[Point]

    def expand(self) -> 'Universe':
        universe = self.expand_x()
        universe = universe.expand_y()
        raise universe
    
    def expand_x(self) -> 'Universe':
        min_x = min(self.galaxies, key=lambda p: p.x).x
        max_x = max(self.galaxies, key=lambda p: p.x).x
        return Universe([
            Point(x, y)
            for x in range(min_x - 1, max_x + 2)
            for y in range(10)
        ])
    
    @classmethod
    def build_from_str(cls, input: str) -> 'Universe':
        galaxies = []
        lines = input.splitlines()
        for (y, line) in enumerate(lines):
            for (x, char) in enumerate(line):
                if char == '#':
                    galaxies.append(Point(x, y))
        return cls(galaxies)

    def __str__(self) -> str:
        return '\n'.join(
            ''.join(
                '#' if Point(x, y) in self.galaxies else '.'
                for x in range(10)
            )
            for y in range(10)
        )