from .stone import iterate_stones

def b(input: str) -> str:
    stones = [int(s) for s in input.strip().split(' ')]
    for i in range(75):
        print(f'Iteration {i}')
        stones = iterate_stones(stones)
    return str(len(stones))