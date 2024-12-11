from .stone import count_of_stones_after_n_iterations

def b(input: str) -> str:
    stones = [int(s) for s in input.strip().split(' ')]
    total_stone_count = 0
    for stone in stones:
        total_stone_count += count_of_stones_after_n_iterations(stone, 75)
    return str(total_stone_count)