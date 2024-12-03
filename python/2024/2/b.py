from itertools import pairwise

def b(input: str) -> str:
    lines = [line for line in input.split("\n") if len(line) > 0]
    safe_lines = [line for line in lines if is_line_safe(line)]
    return str(len(safe_lines))


def is_line_safe(line: str | list[int], try_removing: bool = True) -> bool:
    if isinstance(line, str):
        numbers = [int(n) for n in line.split(" ")]
    else:
        numbers = line
    deltas = [a - b for a, b in pairwise(numbers)]
    if all(1 <= delta <= 3 for delta in deltas):
        return True
    if all(-3 <= delta <= -1 for delta in deltas):
        return True
    # If the line wasn't safe as-is, we can try removing some elements.
    if try_removing:
        for i in range(len(numbers)):
            line_with_removal = numbers[0:i] + numbers[i+1:len(numbers)]
            if is_line_safe(line_with_removal, try_removing=False):
                return True
    return False