from dataclasses import dataclass

@dataclass
class Number:
    value: int
    coords: list[(int, int)]

    def adjacent(self, other: (int, int)) -> bool:
        return any(adjacent(a, other) for a in self.coords)

def adjacent(a: (int, int), b: (int, int)) -> bool:
    return abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1

def b(input: str) -> str:
    numbers: list[Number] = []
    stars: list[(int, int)] = []
    for y, line in enumerate(input.splitlines()):
        x = 0
        while x < len(line):
            char = line[x]
            if char == '*':
                stars.append((x, y))
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
                x += 1
    
    running_gear_ratio_sum = 0
    for star in stars:
        adj_nums = [num for num in numbers if num.adjacent(star)]
        if len(adj_nums) == 2:
            running_gear_ratio_sum += adj_nums[0].value * adj_nums[1].value
            

    return str(running_gear_ratio_sum)