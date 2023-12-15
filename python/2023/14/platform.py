from dataclasses import dataclass
from functools import reduce
from typing import Literal
from operator import xor


Direction = Literal['North', 'East', 'South', 'West']


@dataclass
class Point:
    x: int
    y: int

    def to(self, direction: Direction) -> 'Point':
        match direction:
            case 'North':
                return Point(self.x, self.y - 1)
            case 'South':
                return Point(self.x, self.y + 1)
            case 'West':
                return Point(self.x - 1, self.y)
            case 'East':
                return Point(self.x + 1, self.y)
    
    def set_at(self, p: 'Point'):
        # Update in-place
        self.x = p.x
        self.y = p.y
    
    def fake_hash(self):
        return hash((self.x, self.y))


@dataclass
class Platform:
    width: int
    height: int
    rounded_rocks: list[Point]
    cube_rocks: list[Point]

    def tilt_cyle(self):
        self.tilt('North')
        self.tilt('West')
        self.tilt('South')
        self.tilt('East')

    def tilt(self, direction: Direction):
        # Start at the row/column closest to the direction
        # and move towards the opposite side.
        match direction:
            case 'North':
                sorted_rocks = sorted(self.rounded_rocks, key=lambda p: p.y)
            case 'South':
                sorted_rocks = sorted(self.rounded_rocks, key=lambda p: -p.y)
            case 'West':
                sorted_rocks = sorted(self.rounded_rocks, key=lambda p: p.x)
            case 'East':
                sorted_rocks = sorted(self.rounded_rocks, key=lambda p: -p.x)
        for rock in sorted_rocks:
            self.roll_rock(rock, direction) 

    def roll_rock(self, rock: Point, direction: Direction):
        # While the next position in *direction* is on the board and unoccupied, move the rock.
        while True:
            next_pos = rock.to(direction)
            if next_pos.x >= self.width or next_pos.y >= self.height or next_pos.x < 0 or next_pos.y < 0:
                break
            if next_pos in self.rounded_rocks or next_pos in self.cube_rocks:
                break
            rock.set_at(next_pos)

    @classmethod
    def build_from_str(cls, input: str) -> 'Platform':
        rounded_rocks = []
        cube_rocks = []
        width = 0
        height = 0
        for (y, line) in enumerate(input.splitlines()):
            height += 1
            width = max(width, len(line))
            for (x, char) in enumerate(line):
                if char == 'O':
                    rounded_rocks.append(Point(x, y))
                elif char == '#':
                    cube_rocks.append(Point(x, y))
        return cls(width, height, rounded_rocks, cube_rocks)
    
    def load(self) -> int:
        load = 0
        for rock in self.rounded_rocks:
            load += self.height - rock.y
        return load
    
    def __str__(self):
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                if Point(x, y) in self.rounded_rocks:
                    s += 'O'
                elif Point(x, y) in self.cube_rocks:
                    s += '#'
                else:
                    s += '.'
            s += '\n'
        return s
    
    def rounded_rock_hash(self):
        return reduce(xor, (rock.fake_hash() for rock in self.rounded_rocks))
            