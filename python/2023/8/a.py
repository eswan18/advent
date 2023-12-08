from .game import Game


def a(input: str) -> str:
   game = Game.build_from_str(input)
   steps = game.play()
   return str(steps)