from dataclasses import dataclass
from enum import StrEnum
from collections import Counter


class Direction(StrEnum):
    top = 'top'
    right = 'right'
    bottom = 'bottom'
    left = 'left'

    def opposite(self) -> 'Direction':
        match self:
            case Direction.top:
                return Direction.bottom
            case Direction.right:
                return Direction.left
            case Direction.bottom:
                return Direction.top
            case Direction.left:
                return Direction.right


class Pipe(StrEnum):
    vertical = '|'
    horizontal = '-'
    bend_l = 'L'
    bend_j = 'J'
    bend_7 = '7'
    bend_f = 'F'

    def connectors(self) -> list[Direction]:
        match self:
            case Pipe.vertical:
                return [Direction.top, Direction.bottom]
            case Pipe.horizontal:
                return [Direction.left, Direction.right]
            case Pipe.bend_l:
                return [Direction.top, Direction.right]
            case Pipe.bend_j:
                return [Direction.top, Direction.left]
            case Pipe.bend_7:
                return [Direction.bottom, Direction.left]
            case Pipe.bend_f:
                return [Direction.bottom, Direction.right]
    
    def can_connect_to(self, other: 'Pipe', direction: Direction) -> bool:
        if direction not in self.connectors():
            return False
        if direction.opposite() not in other.connectors():
            return False
        return True
    
    @classmethod
    def chars(cls) -> list[str]:
        return [pipe.value for pipe in cls]
        

@dataclass
class Grid:
    tiles: list[list[Pipe | None]]
    start_position: tuple[int, int] = (0, 0)

    def __str__(self) -> str:
        def tile_as_str(tile: Pipe | None) -> str:
            return tile.value if tile else '.'
        return '\n'.join(''.join(tile_as_str(tile) for tile in row) for row in self.tiles)
    
    @classmethod
    def build_from_str(cls, s: str) -> 'Grid':
        # We parse the pipes and temporarily ignore the starting position, which will
        # be marked as None for now.
        rows = []
        start_pos = None
        for y, line in enumerate(s.splitlines()):
            row = []
            for x, c in enumerate(line):
                if c in Pipe.chars():
                    row.append(Pipe(c))
                else:
                    if c == 'S':
                        start_pos = (x, y)
                    row.append(None)
            rows.append(row)
        # Now we go back and figure out what the starting pipe should have been.
        rows[start_pos[1]][start_pos[0]] = cls.impute_starting_pipe(rows, start_pos)

        return cls(rows, start_pos)
    
    @classmethod
    def impute_starting_pipe(cls, rows: list[list[Pipe | None]], start_pos: tuple[int, int]) -> Pipe:
        x, y = start_pos
        # We need to look at the surrounding tiles to figure out what the starting pipe should be.
        connects_above = False
        if y > 0:
            tile = rows[y - 1][x]
            connects_above = isinstance(tile, Pipe) and Direction.bottom in tile.connectors()
        connects_left = False
        if x > 0:
            tile = rows[y][x - 1]
            connects_left = isinstance(tile, Pipe) and Direction.right in tile.connectors()
        connects_below = False
        if y < len(rows) - 1:
            tile = rows[y + 1][x]
            connects_below = isinstance(tile, Pipe) and Direction.top in tile.connectors()
        connects_right = False
        if x < len(rows[y]) - 1:
            tile = rows[y][x + 1]
            connects_right = isinstance(tile, Pipe) and Direction.left in tile.connectors()
        match (connects_above, connects_left, connects_below, connects_right):
            case (True, False, False, True):
                return Pipe.bend_l
            case (True, True, False, False):
                return Pipe.bend_j
            case (False, True, True, False):
                return Pipe.bend_7
            case (False, False, True, True):
                return Pipe.bend_f
            case (True, False, True, False):
                return Pipe.vertical
            case (False, True, False, True):
                return Pipe.horizontal
            case _:
                raise ValueError(f'Could not impute starting pipe for {start_pos}')
            

@dataclass
class PositionWithDirection:
    position: tuple[int, int]
    direction: Direction

@dataclass
class TraversalState:
    positions: tuple[PositionWithDirection, PositionWithDirection]
    seen: Counter[tuple[int, int]]

    @classmethod
    def build_from_start(cls, start_pos: tuple[int, int], start_pipe: Pipe) -> 'TraversalState':
        match start_pipe:
            case Pipe.vertical:
                a = PositionWithDirection((start_pos[0], start_pos[1] - 1), Direction.top)
                b = PositionWithDirection((start_pos[0], start_pos[1] + 1), Direction.bottom)
            case Pipe.horizontal:
                a = PositionWithDirection((start_pos[0] - 1, start_pos[1]), Direction.left)
                b = PositionWithDirection((start_pos[0] + 1, start_pos[1]), Direction.right)
            case Pipe.bend_l:
                a = PositionWithDirection((start_pos[0], start_pos[1] - 1), Direction.top)
                b = PositionWithDirection((start_pos[0] + 1, start_pos[1]), Direction.right)
            case Pipe.bend_j:
                a = PositionWithDirection((start_pos[0], start_pos[1] - 1), Direction.top)
                b = PositionWithDirection((start_pos[0] - 1, start_pos[1]), Direction.left)
            case Pipe.bend_7:
                a = PositionWithDirection((start_pos[0], start_pos[1] + 1), Direction.bottom)
                b = PositionWithDirection((start_pos[0] - 1, start_pos[1]), Direction.left)
            case Pipe.bend_f:
                a = PositionWithDirection((start_pos[0], start_pos[1] + 1), Direction.bottom)
                b = PositionWithDirection((start_pos[0] + 1, start_pos[1]), Direction.right)
            case _:
                raise ValueError(f'Cannot build traversal state from {start_pos} and {start_pipe}')
        seen = Counter([start_pos, a.position, b.position])
        return cls((a, b), seen)

    def next(self, grid: Grid) -> 'TraversalState':
        next_positions = []
        seen = self.seen
        for position in self.positions:
            next_position = self.next_position(position, grid)
            next_positions.append(next_position)
            seen[next_position.position] += 1
        return TraversalState(tuple(next_positions), self.seen)
    
    def has_looped(self) -> bool:
        return any(count > 1 for count in self.seen.values())
    
    def n_steps(self) -> int:
        return (sum(self.seen.values()) - 1) / 2
    
    def next_position(self, position: PositionWithDirection, grid: Grid) -> PositionWithDirection:
        x, y = position.position
        pipe = grid.tiles[y][x]
        new_direction = [connector for connector in pipe.connectors() if connector != position.direction.opposite()][0]
        match new_direction:
            case Direction.top:
                next_position = (x, y - 1)
            case Direction.right:
                next_position = (x + 1, y)
            case Direction.bottom:
                next_position = (x, y + 1)
            case Direction.left:
                next_position = (x - 1, y)
            case _:
                raise ValueError(f'Cannot get next position from {position}')
        return PositionWithDirection(next_position, new_direction)
