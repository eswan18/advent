from dataclasses import dataclass

@dataclass
class Number:
    value: int
    coords: list[(int, int)]

    def adjacent(self, other: (int, int)) -> bool:
        return any(adjacent(a, other) for a in self.coords)

def adjacent(a: (int, int), b: (int, int)) -> bool:
    return abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1

def a(input: str) -> str:
    numbers: list[Number] = []
    symbols: list[(int, int)] = []
    for y, line in enumerate(input.splitlines()):
        x = 0
        while x < len(line):
            char = line[x]
            if char == '.':
                x += 1
            elif char.isdigit():
                coords = [(x, y)]
                number = line[x]
                x += 1
                while x < len(line) and line[x].isdigit():
                    number += line[x]
                    coords.append((x, y))
                    x += 1
                numbers.append(Number(int(number), coords=coords))
            else:
                symbols.append((x, y))
                x += 1
    
    adj_nums = [num for num in numbers if any(num.adjacent(sym) for sym in symbols)]
    return str(sum(num.value for num in adj_nums))