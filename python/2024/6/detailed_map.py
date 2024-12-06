from typing import Self
from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: Self):
        return self.__class__(
            x=self.x + other.x,
            y=self.y + other.y,
        )

@dataclass(frozen=True)
class OrientedPosition:
    position: Position
    orientation: Position

@dataclass
class DetailedMap:
    obstacles: set[Position]
    guard_at: OrientedPosition
    guard_visited: set[OrientedPosition]
    width: int
    height: int
    has_looped: bool = False

    @classmethod
    def from_str(cls, s: str) -> Self:
        lines = s.strip().split()
        height = len(lines)
        width = len(lines[0])
        obstacles = set()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    position = Position(x, y)
                    obstacles.add(position)
                elif c == '^':
                    guard_at = OrientedPosition(
                        position=Position(x, y),
                        orientation=Position(0, -1),
                    )
        return cls(
            obstacles=obstacles,
            guard_at=guard_at,
            guard_visited={guard_at},
            height=height,
            width=width,
        )

    def advance(self) -> bool:
        '''Advance the guard one step. Returns true if he is still on the board. Returns false otherwise.'''
        # Try to move the guard.
        next_pos = self.guard_at.position + self.guard_at.orientation
        if next_pos in self.obstacles:
            # At obstacles, we just rotate the guard instead of moving.
            self.guard_at = OrientedPosition(self.guard_at.position, rotate_90(self.guard_at.orientation))
            if self.guard_at in self.guard_visited:
                self.has_looped = True
            return True
        if next_pos.x < 0 or next_pos.x >= self.width:
            return False
        if next_pos.y < 0 or next_pos.y >= self.height:
            return False

        self.guard_at = OrientedPosition(next_pos, self.guard_at.orientation)
        if self.guard_at in self.guard_visited:
            self.has_looped = True
        self.guard_visited.add(self.guard_at)
        return True
    
    def __str__(self) -> str:
        visited_positions = [visited.position for visited in self.guard_visited]
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                if Position(x, y) in self.obstacles:
                    s += '#'
                elif Position(x, y) == self.guard_at.position:
                    s += 'G'
                elif Position(x, y) in visited_positions:
                    s += 'X'
                else:
                    s += '.'
            s += '\n'
        return s


def rotate_90(p: Position) -> Position:
    match p:
        case Position(-1, 0):
            return Position(0, -1)
        case Position(0, -1):
            return Position(1, 0)
        case Position(1, 0):
            return Position(0, 1)
        case Position(0, 1):
            return Position(-1, 0)
        case _:
            raise ValueError(f'unexpected direction {p}')
