import sys
from .beam import Grid, BeamGrid, Beam


# Necessary to avoid RecursionErrors when we count all the points at the end, starting
# at the root.
sys.setrecursionlimit(1_000_000)


def a(input: str) -> str:
    grid = Grid.build_from_str(input)
    print(grid)
    print()

    beam_grid = BeamGrid(grid=grid, origin=Beam(at=(0, 0)))

    for i in range(1100):
        if i % 10 == 0:
            # Periodically cull extra beams.
            beam_grid.cull()
        beam_grid.next()
    return str(beam_grid.energized_count())