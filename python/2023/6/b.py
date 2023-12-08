from .race import Race
from functools import reduce

def b(input: str) -> str:
    lines = input.splitlines()
    races = Race.from_lines(lines, merge=True)
    race = races[0]
    ways_to_win = race.ways_to_win()
    return str(ways_to_win)