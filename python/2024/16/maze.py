from __future__ import annotations
import time
from typing import Self
from dataclasses import dataclass


def find_shortest_path(maze: Maze, path: Path | None = None) -> int | None:
    # On the first invocation, create the path.
    if path is None:
        path = Path(points=(maze.start,), score=0, facing=Position(1, 0))
    #print(maze.path_overlay(path))
    #time.sleep(0.5)
    # Base cases: we're at the end or we're stuck.
    if path.points[-1] == maze.end:
        print(path.score)
        return path.score
    if maze[path.points[-1]] == "#":
        return None

    # Decide where we can go next and how much it'll cost.
    # Start by continuing in the direction we're facing, since that's the lowest score.
    next_options: list[tuple[Position, int]] = [(path.facing, 1)]
    if path.facing in (Position(1, 0), Position(-1, 0)):
        next_options.append((Position(0, 1), 1001))
        next_options.append((Position(0, -1), 1001))
    else:  # Position must be in (Position(0, 1), Position(0, -1))
        next_options.append((Position(1, 0), 1001))
        next_options.append((Position(-1, 0), 1001))

    possible_scores: set[int] = set()
    for direction, added_score in next_options:
        next_point = path.points[-1] + direction
        if next_point in path.points:
            # Don't ever loop -- it's never the fastest way.
            continue
        result = find_shortest_path(
            maze,
            path=Path(
                points=path.points + (next_point,),
                score=path.score + added_score,
                facing=direction,
            ),
        )
        if result is not None:
            possible_scores.add(result)
    return min(possible_scores) if len(possible_scores) > 0 else None


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
