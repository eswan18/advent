import re

pattern = re.compile(r'mul\((\d+),(\d+)\)')

def a(input: str) -> str:
    input = input.strip()
    pos = 0
    sum = 0
    while pos < len(input):
        if match := pattern.match(input[pos:]):
            a = int(match.group(1))
            b = int(match.group(2))
            sum += a * b
            pos += match.span()[1]
        else:
            pos += 1
        
    return str(sum)