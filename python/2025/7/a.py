from typing import Self
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Point:
    x: int
    y: int

@dataclass(frozen=True)
class GameBoard:
    height: int
    width: int
    start: Point
    splitters: set[Point]

    @classmethod
    def from_str(cls, s: str) -> Self:
        lines = s.strip().splitlines()
        height = len(lines)
        width = len(lines[0].strip())
        # The start is always in the first line so we can check there and skip the rest.
        start_x = lines[0].find('S')
        if start_x == -1:
            raise RuntimeError
        start = Point(start_x, 0)

        # Now search for splitters in the following lines.
        splitters: set[Point] = set()
        for y, line in enumerate(lines[1:], 1):
            new_pts = set(Point(x, y) for (x, val) in enumerate(line) if val == '^')
            splitters = splitters.union(new_pts)
            
        return cls(height=height, width=width, start=start, splitters=splitters)
    
    def __str__(self) -> str:
        s = []
        for y in range(self.height):
            for x in range(self.width):
                pt = Point(x, y)
                if pt in self.splitters:
                    s.append('^')
                elif pt == self.start:
                    s.append('S')
                else:
                    s.append('.')
            s.append('\n')
        return ''.join(s)


@dataclass(frozen=True)
class GameState:
    board: GameBoard
    current_beam_locations: set[Point]
    all_beam_locations: set[Point]
    split_at: set[Point] = field(default_factory=set)

    @classmethod
    def new_from_board(cls, board: GameBoard) -> Self:
        return cls(
            board=board,
            current_beam_locations={board.start},
            all_beam_locations={board.start},
        )
    
    def step(self) -> Self:
        """Return the next game state after beams take one turn."""
        next_beam_locations = set()
        split_at = set()
        for point in self.current_beam_locations:
            if point in self.board.splitters:
                split_at.add(point)
                # Add left & right
                left = Point(point.x-1, point.y)
                right = Point(point.x+1, point.y)
                if left.x >= 0:
                    next_beam_locations.add(left)
                if right.x < self.board.width:
                    next_beam_locations.add(right)
            else:
                # Just go down one
                next_pt = Point(point.x, point.y+1)
                if next_pt.y < self.board.height:
                    next_beam_locations.add(next_pt)
        return self.__class__(
            board=self.board,
            current_beam_locations=next_beam_locations,
            all_beam_locations=self.all_beam_locations.union(next_beam_locations),
            split_at=self.split_at.union(split_at)
        )
    
    def __str__(self) -> str:
        s = []
        for y in range(self.board.height):
            for x in range(self.board.width):
                pt = Point(x, y)
                if pt in self.board.splitters:
                    s.append('^')
                elif pt == self.board.start:
                    s.append('S')
                elif pt in self.all_beam_locations:
                    s.append('|')
                else:
                    s.append('.')
            s.append('\n')
        return ''.join(s)



def a(input: str) -> str:
    board = GameBoard.from_str(input)
    state = GameState.new_from_board(board)
    while True:
        state = state.step()
        if len(state.current_beam_locations) == 0:
            break
    return str(len(state.split_at))