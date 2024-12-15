from .game import Game


def b(input: str) -> str:
    games = [Game.from_str(s, fix_conv_error=True) for s in input.split("\n\n")]
    cost = 0
    for game in games:
        try:
            cost += game.smart_cost()
        except ValueError:
            pass
    return str(cost)
