from .antenna_map import AntennaMap

def a(input: str) -> str:
    m = AntennaMap.from_string(input)
    print(len(m.antinodes()))