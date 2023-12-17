from heapq import heappush, heappop
from typing import TypeAlias
from dataclasses import dataclass, field

from .direction import Direction
from .grid import Grid, Position


Distance: TypeAlias = int


@dataclass(order=True, frozen=True)
class Move:
    distance: Distance
    from_: Position
    to: Position
    recent_directions: tuple[Direction | None, Direction | None, Direction | None]
    last: 'Move | None' = field(default=None)

    def __str__(self) -> str:
        return f"{self.distance}: {self.from_} {self.recent_directions[-1]} {self.to}"


@dataclass
class Traversal:
    """
    A traversal is a short-path algorithm traversal of a grid.

    The "distance" between nodes is the value of the node being traveled to.
    We use a heap to store places we've been so far, along with their distance, and pop
    the heap to get the position that currently has the closest distance. We add all
    valid next positions from that position (along with their distances) back to the
    heap and repeat, until we hit the ending node.
    """
    start: Position
    end: Position
    grid: Grid
    # This is used as a heap, so we can always pull the smallest element.
    next_moves: list[Move] = field(init=False)
    # This is a way to keep track of positions we've seen before, so we don't come back unless we find a shorter path.
    seen: set[tuple, Position, tuple[Direction | None, Direction | None, Direction | None]] = field(init=False)

    def __post_init__(self):
        self.next_moves = []
        for direction, position in self.grid.connecting_points(self.start):
            distance = self.grid.heat_loss[position]
            recent_directions = (None, None, direction)
            heappush(self.next_moves, Move(distance, self.start, position, recent_directions))
        self.seen = {self.start}
    
    def __str__(self) -> str:
        s = ''
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if Position(x, y) == self.start:
                    s += "S"
                elif Position(x, y) == self.end:
                    s += "E"
                elif Position(x, y) in self.seen:
                    s += "X"
                else:
                    s += " "
            s += "\n"
        return s
    
    def _iterate(self) -> Move | None:
        # Grab the closest position we've seen so far.
        next_move = heappop(self.next_moves)
        if (next_move.to, next_move.recent_directions) in self.seen:
            return None
        # Add it to the seen list.
        self.seen.add((next_move.to, next_move.recent_directions))
        # We can't go backward, so determine what that direction is.
        cant_go = {next_move.recent_directions[-1].opposite()}
        # If this move has now led us to go three times in the same direction, we also
        # need to remember not to go that way again.
        if len(set(next_move.recent_directions)) == 1:
            cant_go.add(next_move.recent_directions[0])

        # Add all valid next positions to the heap.
        for direction, position in self.grid.connecting_points(next_move.to):
            if direction in cant_go:
                continue
            distance = next_move.distance + self.grid.heat_loss[position]
            recent_directions = next_move.recent_directions[1:] + (direction,)
            heappush(self.next_moves, Move(distance, next_move.to, position, recent_directions, last=next_move))
        return next_move

    def find_path(self) -> int:
        """
        Find the shortest path from the start to the end.
        """
        while True:
            match self._iterate():
                case None:
                    continue
                case move:
                    if move.to == self.end:
                        return move.distance
    
    def move_history_str(self, move: Move) -> str:
        """
        Return a string showing the path that led to this move.
        """
        positions_and_directions = {}
        while move:
            positions_and_directions[move.to] = move.recent_directions[-1]
            move = move.last
        positions_and_directions[self.start] = 'S'
        s = ''
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                direction = positions_and_directions.get(Position(x, y))
                if direction is not None:
                    s += str(direction)
                else:
                    s += " "
            s += "\n" 
        return s