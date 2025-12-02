DIAL_START = 50


def b(input: str) -> str:
    dial = DIAL_START
    stops_at_0 = 0
    for line in input.splitlines():
        direction = line[0]
        value = int(line[1:].strip())
        
        turns, value = divmod(value, 100)
        stops_at_0 += turns
        if dial == 0 and direction == 'L':
            # Horrible hack, but lets get away with double-counting cases when the dial lands on 0 and then spins left.
            stops_at_0 -= 1

        if direction == 'R':
            dial += value
        else:
            dial -= value

        if dial == 0:
            stops_at_0 += 1
        if dial < 0:
            dial += 100
            stops_at_0 += 1
        if dial >= 100:
            dial -= 100
            stops_at_0 += 1
    return stops_at_0
