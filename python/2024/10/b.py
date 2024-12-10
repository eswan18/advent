from .topographic_map import TopographicMap


def b(input: str) -> str:
    tm = TopographicMap.from_str(input)
    running_sum = 0
    for nadir in tm.nadirs():
        score = tm.trailhead_rating(nadir)
        running_sum += score
    return str(running_sum)