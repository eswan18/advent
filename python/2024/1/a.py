def a(input: str) -> str:
    lines = input.splitlines()
    column_a = []
    column_b = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        a, b = line.split()
        column_a.append(int(a))
        column_b.append(int(b))
    column_a.sort()
    column_b.sort()
    total_diff = 0
    for a, b in zip(column_a, column_b):
        total_diff += abs(a - b)
    return str(total_diff)
