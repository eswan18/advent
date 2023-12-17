from dataclasses import dataclass
from .direction import Direction

@dataclass(slots=True, frozen=True, order=True)
class Position:
    x: int
    y: int
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass
class Grid:
    heat_loss: dict[Position, int]
    width: int
    height: int

    @classmethod
    def from_str(cls, input: str) -> 'Grid':
        heat_loss = {}
        for y, line in enumerate(input.splitlines()):
            for x, char in enumerate(line):
                heat_loss[Position(x, y)] = int(char)
        return cls(heat_loss, x + 1, y + 1)
    
    def __str__(self) -> str:
        return "\n".join(
            "".join(str(self.heat_loss[Position(x, y)]) for x in range(self.width))
            for y in range(self.height)
        )
    
    def connecting_points(self, point: Position) -> list[tuple[Direction, Position]]:
        possible = [
            (Direction.RIGHT, Position(point.x + 1, point.y)),
            (Direction.LEFT, Position(point.x - 1, point.y)),
            (Direction.DOWN, Position(point.x, point.y + 1)),
            (Direction.UP, Position(point.x, point.y - 1)),
        ]
        return [p for p in possible if p[1] in self.heat_loss]