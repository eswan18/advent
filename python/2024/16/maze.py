from __future__ import annotations
import time
from heapq import heappop, heappush
from typing import Self
from dataclasses import dataclass


def find_shortest_path(maze: Maze) -> int | None:
    path_heap = [Path(points=(maze.start,), score=0, facing=Position(1, 0))]
    # All the points and facing directions we've already seen, to avoid traversing over
    # the same point twice.
    seen_before: set[tuple[Position, Position]] = set()

    while path_heap:
        shortest_path = heappop(path_heap)
        last_pt = shortest_path.points[-1]
        if maze[last_pt] == '#':
            # If this path ends at a wall, it's a dead end.
            continue
        if last_pt == maze.end:
            # If this path ends and END, we found the shortest path.
            return shortest_path.score
        # Otherwise, find all the next steps for this path, and add them to the heap.
        next_options: list[tuple[Position, int]] = [(shortest_path.facing, 1)]
        if shortest_path.facing in (Position(1, 0), Position(-1, 0)):
            # Turn from horizontal to vertical.
            next_options.append((Position(0, 1), 1001))
            next_options.append((Position(0, -1), 1001))
        else:  # Position must be in (Position(0, 1), Position(0, -1))
            # Turn from vertical to horizontal.
            next_options.append((Position(1, 0), 1001))
            next_options.append((Position(-1, 0), 1001))
        for direction, added_score in next_options:
            next_point = shortest_path.points[-1] + direction
            if (next_point, direction) in seen_before:
                # Skip point/direction combos we've already seen
                continue
            next_path = Path(
                points=shortest_path.points + (next_point,),
                score=shortest_path.score + added_score,
                facing=direction,
            )
            heappush(path_heap, next_path)
            seen_before.add((next_point, direction))


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return self.__class__(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return self.__class__(x=self.x - other.x, y=self.y - other.y)


@dataclass(frozen=True)
class Path:
    points: tuple[Position, ...]
    score: int
    facing: Position

    def __str__(self) -> str:
        return ",".join(f"({pt.x}, {pt.y})" for pt in self.points)
    
    def __lt__(self, other: Self) -> bool:
        if not isinstance(other, Path):
            return NotImplemented
        return self.score < other.score


@dataclass
class Maze:
    walls: set[Position]
    start: Position
    end: Position
    width: int
    height: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        start = None
        end = None
        walls: set[Position] = set()
        for y, line in enumerate(s.splitlines()):
            for x, c in enumerate(line):
                match c:
                    case "#":
                        walls.add(Position(x, y))
                    case "S":
                        start = Position(x, y)
                    case "E":
                        end = Position(x, y)
                width = x + 1
            height = y + 1
        return cls(walls=walls, start=start, end=end, width=width, height=height)

    def __getitem__(self, key: Position) -> str:
        if key == self.start:
            return "S"
        if key in self.walls:
            return "#"
        else:
            return "."

    def __str__(self) -> str:
        s = ""
        for y in range(self.height):
            for x in range(self.width):
                s += self[Position(x, y)]
            s += "\n"
        return s

    def path_overlay(self, path: Path) -> str:
        s = ""
        for y in range(self.height):
            for x in range(self.width):
                thing = self[Position(x, y)]
                if thing == "." and Position(x, y) in path.points:
                    s += "X"
                else:
                    s += thing
            s += "\n"
        return s
