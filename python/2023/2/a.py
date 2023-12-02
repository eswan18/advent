from .draw import Draw, Game

TEST = Draw(12, 14, 13)
        

def a(input: str) -> str:
    id_sum = 0
    for line in input.splitlines():
        game = Game.from_str(line)
        if game.possible_from_draw(TEST):
            id_sum += game.id
    return str(id_sum)