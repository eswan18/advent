DIAL_START = 50


def a(input: str) -> str:
    dial = DIAL_START
    stops_at_0 = 0
    for line in input.splitlines():
        if dial == 0:
            stops_at_0 += 1
        direction = line[0]
        value = int(line[1:].strip())
        value %= 100
        if direction == 'R':
            dial += value
        else:
            dial -= value
        if dial < 0:
            dial += 100
        elif dial >= 100:
            dial -= 100
    return stops_at_0
