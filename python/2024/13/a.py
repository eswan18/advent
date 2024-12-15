from .game import Game

def a(input: str) -> str:
    games = [Game.from_str(s) for s in input.split('\n\n')]
    cost = 0
    for game in games:
        try:
            cost += game.cost()
        except ValueError:
            pass
    return str(cost)