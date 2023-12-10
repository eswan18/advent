from .pipe import Grid


def a(input: str) -> str:
    grid = Grid.build_from_str(input)
    print(grid)