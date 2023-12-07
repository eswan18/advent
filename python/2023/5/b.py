from .parse import parse


def b(input: str) -> str:
    game = parse(input, seeds_type='range')