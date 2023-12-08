from functools import reduce

from .race import Race

def a(input: str) -> str:
    lines = input.splitlines()
    races = Race.from_lines(lines)
    ways_to_win = [r.ways_to_win() for r in races]
    print(ways_to_win)
    product = reduce(lambda x, y: x * y, ways_to_win)
    return str(product)