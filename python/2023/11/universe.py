from dataclasses import dataclass
from typing import NamedTuple
from itertools import combinations

class Point(NamedTuple):
    x: int
    y: int

    def manhattan_dist(self, other: 'Point') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

@dataclass
class Universe:
    galaxies: list[Point]

    def expand(self, factor: int = 2) -> 'Universe':
        expanded_x = self.expand_x(factor)
        expanded_all = expanded_x.expand_y(factor)
        return expanded_all
    
    def expand_x(self, factor: int) -> 'Universe':
        # Find empty columns.
        x_values = set(point.x for point in self.galaxies)
        n_cols = max(x_values) + 1
        empty_cols = set(range(n_cols)) - x_values
        new_points = []
        for point in self.galaxies:
            # How many empty columns are there to the left of this point?
            adjust_factor = len([col for col in empty_cols if col < point.x])
            adjust_factor *= (factor - 1)
            new_points.append(Point(point.x + adjust_factor, point.y))
        return Universe(new_points)

    def expand_y(self, factor: int) -> 'Universe':
        # Find empty rows.
        y_values = set(point.y for point in self.galaxies)
        n_rows = max(y_values) + 1
        empty_rows = set(range(n_rows)) - y_values
        new_points = []
        for point in self.galaxies:
            # How many empty rows are there above this point?
            adjust_factor = len([row for row in empty_rows if row < point.y])
            adjust_factor *= (factor - 1)
            new_points.append(Point(point.x, point.y + adjust_factor))
        return Universe(new_points)
    
    def all_galaxy_pairs(self) -> list[tuple[Point, Point]]:
        return list(combinations(self.galaxies, 2))
    
    def sum_of_all_distances(self) -> int:
        pairs = self.all_galaxy_pairs()
        distances = [pair[0].manhattan_dist(pair[1]) for pair in pairs]
        return sum(distances)
    
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
        max_x = max(point.x for point in self.galaxies)
        max_y = max(point.y for point in self.galaxies)
        s = ''
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if Point(x, y) in self.galaxies:
                    s += '#'
                else:
                    s += '.'
            s += '\n'
        return s