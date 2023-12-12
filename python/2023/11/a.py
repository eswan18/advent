from .universe import Universe


def a(input: str) -> str:
    universe = Universe.build_from_str(input)
    universe = universe.expand()
    total_sum = universe.sum_of_all_distances()
    return str(total_sum)