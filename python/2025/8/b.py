from collections import Counter
from typing import Self
from dataclasses import dataclass

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
    current_beam_locations: Counter[Point]
    all_beam_locations: Counter[Point]
    n_splits: int = 0

    @classmethod
    def new_from_board(cls, board: GameBoard) -> Self:
        return cls(
            board=board,
            current_beam_locations=Counter([board.start]),
            all_beam_locations=Counter([board.start]),
        )
    
    def step(self) -> Self:
        next_beam_locations: Counter[Point] = Counter()
        n_splits = 0
        for point, count in self.current_beam_locations.items():
            if point in self.board.splitters:
                n_splits += count
                # Add left & right
                left = Point(point.x-1, point.y)
                right = Point(point.x+1, point.y)
                if left.x >= 0:
                    next_beam_locations[left] += count
                if right.x < self.board.width:
                    next_beam_locations[right] += count
            else:
                # Just go down one
                next_pt = Point(point.x, point.y+1)
                if next_pt.y < self.board.height:
                    next_beam_locations[next_pt] += count
        return self.__class__(
            board=self.board,
            current_beam_locations=next_beam_locations,
            all_beam_locations=self.all_beam_locations + next_beam_locations,
            n_splits=self.n_splits + n_splits
        )
    
    def __str__(self) -> str:
        s = []
        for y in range(self.board.height):
            for x in range(self.board.width):
                pt = Point(x, y)
                if pt in self.board.splitters:
                    s.append('  ^  ')
                elif pt == self.board.start:
                    s.append('  S  ')
                elif pt in self.all_beam_locations:
                    s.append(f' {self.all_beam_locations[pt]:02}_ ')
                else:
                    s.append('  .  ')
            s.append('\n')
        return ''.join(s)



def b(input: str) -> str:
    board = GameBoard.from_str(input)
    state = GameState.new_from_board(board)
    while True:
        state = state.step()
        if len(state.current_beam_locations) == 0:
            break
    # Sum up the number of times we got to any point in the bottom row.
    bottom_row_counts = [
        count for (pt, count) in state.all_beam_locations.items()
        if pt.y == (board.height - 1)
    ]
    return str(sum(bottom_row_counts))