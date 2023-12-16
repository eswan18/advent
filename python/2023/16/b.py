from .beam import Grid, BeamGrid, Beam


def b(input: str) -> str:
    grid = Grid.build_from_str(input)

    # Construct a list of all the points that are on the edge of the grid, along with an
    # off-the-grid point to serve as their origin.
    edge_points: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for x in range(grid.width):
        # The top and bottom.
        edge_points.append(((x, 0), (x, -1)))
        edge_points.append(((x, grid.height - 1), (x, grid.height)))
    for y in range(grid.height):
        # The left and right.
        edge_points.append(((0, y), (-1, y)))
        edge_points.append(((grid.width - 1, y), (grid.width, y)))

    # Find the point & origin point that has the highest energy.
    highest_energy = -1
    for edge_point, origin in edge_points:
        beam_grid = BeamGrid(grid=grid, origin=Beam(at=edge_point, parent_origin=origin))
        while len(beam_grid.active) > 0:
            beam_grid.next()
        highest_energy = max(highest_energy, beam_grid.energized_count())

    return str(highest_energy)