import re

mul_pattern = re.compile(r'mul\((\d+),(\d+)\)')
do_pattern = re.compile(f'do\(\)')
dont_pattern = re.compile(f"don't\(\)")

def b(input: str) -> str:
    input = input.strip()
    pos = 0
    sum = 0
    enabled = True
    while pos < len(input):
        if match := mul_pattern.match(input[pos:]):
            if enabled:
                a = int(match.group(1))
                b = int(match.group(2))
                sum += a * b
            pos += match.span()[1]
        elif do_pattern.match(input[pos:]):
            enabled = True
            pos += 4
        elif dont_pattern.match(input[pos:]):
            enabled = False
            pos += 7
        else:
            pos += 1
        
    return str(sum)