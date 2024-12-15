from typing import Self
from dataclasses import dataclass
from collections import Counter


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        # strings look like "v=2,-58" or "p=-43,81"
        x_str, y_str = s[2:].split(",")
        x, y = int(x_str), int(y_str)
        return cls(x, y)
    
    def __add__(self, other: Self) -> Self:
        return self.__class__(self.x + other.x, self.y + other.y)
    
    def __mul__(self, multiplier: int) -> Self:
        return self.__class__(self.x * multiplier, self.y * multiplier)
    
    def reduce(self, width: int, height: int) -> Self:
        return self.__class__(self.x % width, self.y % height)


@dataclass
class Robot:
    at: Position
    velocity: Position

    @classmethod
    def from_str(cls, s: str) -> Self:
        # strings look like "p=2,-58 v=-43,81"
        pos_str, velo_str = s.split(" ")
        at = Position.from_str(pos_str)
        velocity = Position.from_str(velo_str)
        return cls(at, velocity)


@dataclass
class RobotGrid:
    robots: list[Robot]
    width: int
    height: int

    @classmethod
    def from_str(cls, s: str, width: int, height: int) -> Self:
        robots = [Robot.from_str(line) for line in s.splitlines()]
        return cls(robots=robots, width=width, height=height)

    def iterate_n_seconds(self, n: int):
        for robot in self.robots:
            robot.at = robot.at + robot.velocity * n
            # Account for looping back whenever the robot traverses an edge.
            robot.at = robot.at.reduce(self.width, self.height)
            
    def counts_by_quadrant(self) -> tuple[int, int, int, int]:
        positions = Counter(robot.at for robot in self.robots)
        top_left = sum(
            count for pos, count in positions.items()
            if pos.x < self.width // 2 and pos.y < self.height // 2
        )
        top_right = sum(
            count for pos, count in positions.items()
            if pos.x > self.width // 2 and pos.y < self.height // 2
        )
        bottom_left = sum(
            count for pos, count in positions.items()
            if pos.x < self.width // 2 and pos.y > self.height // 2
        )
        bottom_right = sum(
            count for pos, count in positions.items()
            if pos.x > self.width // 2 and pos.y > self.height // 2
        )
        return top_left, top_right, bottom_left, bottom_right
    
    def safety_factor(self) -> int:
        counts = self.counts_by_quadrant()
        return counts[0] * counts[1] * counts[2] * counts[3]
    
    def is_symmetric(self) -> bool:
        counts = self.counts_by_quadrant()
        return counts[0] == counts[3] and counts[1] == counts[2]
    
    def __str__(self) -> str:
        positions = Counter(robot.at for robot in self.robots)
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                if count := positions.get(Position(x, y)):
                    s += str(count)
                else:
                    s += '.'
            s += '\n'
        return s