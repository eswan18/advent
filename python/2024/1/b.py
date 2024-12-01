from collections import Counter

def b(input: str) -> str:
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
    a = Counter(column_a)
    b = Counter(column_b)

    running_sum = 0
    for key in a:
        running_sum += a[key] * b[key] * key
    return str(running_sum)