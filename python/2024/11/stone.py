def iterate_stone(stone: int) -> list[int]:
    """Turn a stone into the next stone or stones."""
    if stone == 0:
        return [1]
    stone_as_string = str(stone)
    stone_len = len(stone_as_string)
    if stone_len % 2 == 0:
        halfway = stone_len // 2
        left = int(stone_as_string[:halfway])
        right = int(stone_as_string[halfway:])
        return [left, right]
    return [stone * 2024]

def iterate_stones(stones: list[int]) -> list[int]:
    """Turn a list of stones into the next list of stones."""
    next_stones = []
    for stone in stones:
        next_stones.extend(iterate_stone(stone))
    return next_stones