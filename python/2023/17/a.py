from .grid import Grid, Position
from .traversal import Traversal


def a(input: str) -> str:
    grid = Grid.from_str(input)
    traversal = Traversal(
        start=Position(0, 0),
        end=Position(grid.width - 1, grid.height - 1),
        grid=grid,
    )
    distance = traversal.find_path()
    return distance