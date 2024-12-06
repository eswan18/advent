from copy import deepcopy
from .detailed_map import DetailedMap, Position


def b(input: str) -> str:
    start_map = DetailedMap.from_str(input)
    loops = 0
    # This will halt when the guard tries to step out of the map.
    for y in range(start_map.height):
        for x in range(start_map.width):
            pos = Position(x, y)
            if pos in start_map.obstacles:
                continue
            # Add an obstacle to the map and see if it loops.
            current_map = deepcopy(start_map)
            current_map.obstacles.add(pos)
            
            # Play out the map and see if it loops.
            while current_map.advance():
                if current_map.has_looped:
                    loops += 1
                    break
        print(f'Done with row {y} of {start_map.height}')
    return str(loops)