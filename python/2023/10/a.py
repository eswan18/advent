from .pipe import Grid, TraversalState


def a(input: str) -> str:
    grid = Grid.build_from_str(input)
    state = TraversalState.build_from_start(grid.start_position, grid.tiles[grid.start_position[1]][grid.start_position[0]])
    while True:
        state = state.next(grid)
        if state.has_looped():
            return str(state.n_steps())