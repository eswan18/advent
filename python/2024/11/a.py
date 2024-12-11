from .stone import iterate_stones

def a(input: str) -> str:
    stones = [int(s) for s in input.strip().split(' ')]
    for _ in range(25):
        stones = iterate_stones(stones)
    return str(len(stones))