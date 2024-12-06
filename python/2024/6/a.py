from .map import Map

def a(input: str) -> str:
    start_map = Map.from_str(input)
    current_map = start_map
    # This will halt when the guard tries to step out of the map.
    while current_map.advance():
        ...
    return len(current_map.guard_visited)