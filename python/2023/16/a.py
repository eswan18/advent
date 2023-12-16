from .beam import Grid, BeamGrid, Beam


def a(input: str) -> str:
    grid = Grid.build_from_str(input)
    beam_grid = BeamGrid(grid=grid, origin=Beam(at=(0, 0), parent_origin=(-1, 0)))

    while len(beam_grid.active) > 0:
        beam_grid.next()

    return str(beam_grid.energized_count())