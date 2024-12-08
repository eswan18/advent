from .antenna_map import AntennaMap

def a(input: str) -> str:
    m = AntennaMap.from_string(input)
    antinode_count = len(m.antinodes())
    return str(antinode_count)