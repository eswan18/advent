from dataclasses import dataclass
from enum import StrEnum


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