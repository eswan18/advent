from .detailed_map import DetailedMap


def b(input: str) -> str:
    start_map = DetailedMap.from_str(input)
    current_map = start_map
    # This will halt when the guard tries to step out of the map.
    while current_map.advance():
        ...
    uniq_visited_positions = {p.position for p in current_map.guard_visited}
    return len(uniq_visited_positions)