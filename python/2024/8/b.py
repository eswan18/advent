from .antenna_map import AntennaMap

def b(input: str) -> str:
    m = AntennaMap.from_string(input)
    antinode_count = len(m.antinodes_part_b())
    return str(antinode_count)