from itertools import pairwise

def a(input: str) -> str:
    lines = [line for line in input.split("\n") if len(line) > 0]
    safe_lines = [line for line in lines if is_line_safe(line)]
    return str(len(safe_lines))


def is_line_safe(line: str) -> bool:
    numbers = [int(n) for n in line.split(" ")]
    deltas = [a - b for a, b in pairwise(numbers)]
    if all(1 <= delta <= 3 for delta in deltas):
        return True
    if all(-3 <= delta <= -1 for delta in deltas):
        return True
    return False