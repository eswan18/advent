from .game import Game


def b(input: str) -> str:
   game = Game.build_from_str(input, end_node_type="Z")
   print(game.find_repeat_interval("AAA"))