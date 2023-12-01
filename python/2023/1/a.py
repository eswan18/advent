def a(input: str) -> str:
    running_sum = 0
    for line in input.splitlines():
        if len(line) == 0:
            continue
        digits = [c for c in line if c.isdigit()]
        running_sum += 10 * int(digits[0]) + int(digits[-1])
    
    return str(running_sum)
