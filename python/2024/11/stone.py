import functools

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

@functools.lru_cache(1024)
def count_of_stones_after_n_iterations(starting_stone: int, iterations: int) -> int:
    if iterations == 0:
        return 1
    if starting_stone == 0:
        return count_of_stones_after_n_iterations(1, iterations - 1)
    stone_as_string = str(starting_stone)
    stone_len = len(stone_as_string)
    if stone_len % 2 == 0:
        halfway = stone_len // 2
        left = int(stone_as_string[:halfway])
        right = int(stone_as_string[halfway:])
        left_result = count_of_stones_after_n_iterations(left, iterations - 1)
        right_result = count_of_stones_after_n_iterations(right, iterations - 1)
        return left_result + right_result
    return count_of_stones_after_n_iterations(starting_stone * 2024, iterations - 1)