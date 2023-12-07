from .parse import parse


def a(input: str) -> str:
    game = parse(input)
    game.reduce()
    locations = game.get_final_translations()
    return str(min(locations))