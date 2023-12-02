from .draw import Draw, Game
        

def b(input: str) -> str:
    power_sum = 0
    for line in input.splitlines():
        game = Game.from_str(line)
        min_draw = game.minimum_possible_draw()
        power = min_draw.power()
        power_sum += power
    return str(power_sum)