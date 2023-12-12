from .universe import Universe


def a(input: str) -> str:
    print(input)
    universe = Universe.build_from_str(input)
    print(universe)