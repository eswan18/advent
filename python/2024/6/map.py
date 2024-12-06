from typing import Self
from dataclasses import dataclass

@dataclass
class Map:
    obstacles: set[tuple[int, int]] # (x, y) coordinates where obstacles are
    guard_at: tuple[int, int]
    guard_direction: tuple[int, int] # the guard's direction, as an (x, y) vector
    guard_visited: set[tuple[int, int]] # locations the guard has visited
    width: int
    height: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        lines = s.strip().split()
        height = len(lines)
        width = len(lines[0])
        obstacles = set()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    obstacles.add((x, y))
                elif c == '^':
                    guard_at = (x, y)
        return cls(
            obstacles=obstacles,
            guard_at=guard_at,
            guard_direction=(0, -1), # we know the guard is facing up to start.
            guard_visited={guard_at},
            height=height,
            width=width,
        )

    def advance(self) -> bool:
        '''Advance the guard one step. Returns true if he is still on the board. Returns false otherwise.'''
        # Try to move the guard.
        next_pos = (self.guard_at[0] + self.guard_direction[0], self.guard_at[1] + self.guard_direction[1])
        if next_pos in self.obstacles:
            # At obstacles, we just rotate the guard instead of moving.
            self.guard_direction = rotate_90(self.guard_direction)
            return True
        next_x, next_y = next_pos
        if next_x < 0 or next_x >= self.width:
            return False
        if next_y < 0 or next_y >= self.height:
            return False

        self.guard_visited.add(next_pos)
        self.guard_at = next_pos
        return True
    
    def __str__(self) -> str:
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.obstacles:
                    s += '#'
                elif (x, y) == self.guard_at:
                    s += 'G'
                elif (x, y) in self.guard_visited:
                    s += 'X'
                else:
                    s += '.'
            s += '\n'
        return s


def rotate_90(coord: tuple[int, int]) -> tuple[int, int]:
    match coord:
        case (-1, 0):
            return (0, -1)
        case (0, -1):
            return (1, 0)
        case (1, 0):
            return (0, 1)
        case (0, 1):
            return (-1, 0)
        case _:
            raise ValueError(f'unexpected coord {coord}')
