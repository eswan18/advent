from dataclasses import dataclass, field
from typing import Literal

@dataclass
class Mirror:
    mirror: Literal['/', '\\']

    def __str__(self) -> str:
        return self.mirror

@dataclass
class Splitter:
    splitter: Literal['|', '-']

    def __str__(self) -> str:
        return self.splitter
    

@dataclass
class Beam:
    at: tuple[int, int]
    parent: 'Beam | None' = None
    next: list['Beam'] = field(default_factory=list)

    def add_child_at(self, at: tuple[int, int]) -> 'Beam':
        child = Beam(at=at, parent=self)
        self.next.append(child)
        return child
    
    def next_positions(self, grid: 'Grid') -> list[tuple[int, int]]:
        # The first position doesn't have a parent but always comes from the left into (0, 0), so we hardcode that parent.
        parent = self.parent or Beam(at=(-1, 0))
        # Figure out which direction we're coming from.
        d_x, d_y = self.at[0] - parent.at[0], self.at[1] - parent.at[1]
        next = []
        match (d_x, d_y):
            case (0, 1):
                match grid[self.at]:
                    # Coming from above.
                    case '.' | Splitter('|'):
                        # Keep going down.
                        next.append((self.at[0], self.at[1] + 1))
                    case Mirror('/'):
                        # Go left.
                        next.append((self.at[0] - 1, self.at[1]))
                    case Mirror('\\'):
                        # Go right.
                        next.append((self.at[0] + 1, self.at[1]))
                    case Splitter('-'):
                        # Go both left and right.
                        next.append((self.at[0] - 1, self.at[1]))
                        next.append((self.at[0] + 1, self.at[1]))
                    case _:
                        raise RuntimeError(f'Unexpected item {grid[self.at]} at {self.at}') 
            case (0, -1):
                # Coming from below.
                match grid[self.at]:
                    case '.' | Splitter('|'):
                        # Keep going up.
                        next.append((self.at[0], self.at[1] - 1))
                    case Mirror('/'):
                        # Go right.
                        next.append((self.at[0] + 1, self.at[1]))
                    case Mirror('\\'):
                        # Go left.
                        next.append((self.at[0] - 1, self.at[1]))
                    case Splitter('-'):
                        # Go both left and right.
                        next.append((self.at[0] - 1, self.at[1]))
                        next.append((self.at[0] + 1, self.at[1]))
                    case _:
                        raise RuntimeError(f'Unexpected item {grid[self.at]} at {self.at}') 
            case (1, 0):
                # Coming from the left.
                match grid[self.at]:
                    case '.' | Splitter('-'):
                        # Keep going right.
                        next.append((self.at[0] + 1, self.at[1]))
                    case Mirror('/'):
                        # Go up.
                        next.append((self.at[0], self.at[1] - 1))
                    case Mirror('\\'):
                        # Go down.
                        next.append((self.at[0], self.at[1] + 1))
                    case Splitter('|'):
                        # Go both up and down.
                        next.append((self.at[0], self.at[1] - 1))
                        next.append((self.at[0], self.at[1] + 1))
                    case _:
                        raise RuntimeError(f'Unexpected item {grid[self.at]} at {self.at}') 
            case (-1, 0):
                # Coming from the right.
                match grid[self.at]:
                    case '.' | Splitter('-'):
                        # Keep going left.
                        next.append((self.at[0] - 1, self.at[1]))
                    case Mirror('/'):
                        # Go down.
                        next.append((self.at[0], self.at[1] + 1))
                    case Mirror('\\'):
                        # Go up.
                        next.append((self.at[0], self.at[1] - 1))
                    case Splitter('|'):
                        # Go both up and down.
                        next.append((self.at[0], self.at[1] - 1))
                        next.append((self.at[0], self.at[1] + 1))
                    case _:
                        raise RuntimeError(f'Unexpected item {grid[self.at]} at {self.at}') 
            case _:
                raise RuntimeError(f'Unexpected direction {d_x}, {d_y}')
        return next
        
    def add_next_children(self, grid: 'Grid') -> list['Beam']:
        next_positions = self.next_positions(grid)
        # Trim any positions that aren't on the grid.
        next_positions = [
            position for position in next_positions
            if 0 <= position[0] < grid.width and 0 <= position[1] < grid.height
        ]
        next_children = []
        for position in next_positions:
            child = self.add_child_at(position)
            next_children.append(child)
        return next_children
    
    def all_points(self) -> list[tuple[int, int]]:
        points = [self.at]
        for child in self.next:
            points.extend(child.all_points())
        return points


@dataclass
class Grid:
    width: int
    height: int
    items: list[list[Literal['.'] | Mirror | Splitter]]

    @classmethod
    def build_from_str(cls, input: str) -> 'Grid':
        items = []
        for (y, line) in enumerate(input.splitlines()):
            if y == 0:
                width = len(line)
            row = []
            for (x, char) in enumerate(line):
                if char == '.':
                    row.append('.')
                elif char in ['/', '\\']:
                    row.append(Mirror(char))
                elif char in ['|', '-']:
                    row.append(Splitter(char))
                else:
                    raise ValueError(f'Unknown character {char}')
            items.append(row)
        return Grid(height=y+1, width=width, items=items)
    
    def __getitem__(self, key: tuple[int, int]) -> Literal['.'] | Mirror | Splitter:
        return self.items[key[1]][key[0]]
    
    def __str__(self) -> str:
        return '\n'.join(''.join(str(item) for item in row) for row in self.items)


@dataclass
class BeamGrid:
    origin: Beam
    grid: Grid
    active: list[Beam] = field(default_factory=list)

    def next(self) -> None:
        new_active = []
        for beam in self.active:
            next = beam.add_next_children(self.grid)
            new_active.extend(next)
        self.active = new_active

    def __post_init__(self) -> None:
        self.active.append(self.origin)

    def __str__(self) -> str:
        s = 'Active: ' + ','.join(str(beam.at) for beam in self.active) + '\n'
        grid_items = [[item for item in row] for row in self.grid.items]
        for (x, y) in self.origin.all_points():
            grid_items[y][x] = 'X'
        return s + '\n'.join(''.join(str(item) for item in row) for row in grid_items)
    
    def energized_count(self) -> int:
        return len(set(self.origin.all_points()))
    
    def cull(self):
        self.cull_active_duplicates()
        # Todo: cull loops
    
    def cull_active_duplicates(self):
        new_active = []
        # Keep track of active positions and their parents.
        # If two active positions exist with the same parent, we can make one inactive.
        seen: set[(int, int), (int, int) | None] = set()
        for beam in self.active:
            parent_at = beam.parent.at if beam.parent else None
            if (beam.at, parent_at) in seen:
                # This position has already been seen with this parent.
                continue
            seen.add((beam.at, parent_at))
            new_active.append(beam)
        self.active = new_active

    def cull_loop(self):
        new_active = []
        # Keep track of positions and their parents. If this pair has *ever* occurred
        # before in any path, we can inactivate it.
        seen: set[(int, int), (int, int) | None] = set()
        for beam in self.active:
            if beam.at in seen:
                continue
            seen.add(beam.at)
            new_active.append(beam)
        self.active = new_active