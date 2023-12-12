from .universe import Universe


def b(input: str) -> str:
    universe = Universe.build_from_str(input)
    universe = universe.expand(factor=1000000)
    total_sum = universe.sum_of_all_distances()
    return str(total_sum)