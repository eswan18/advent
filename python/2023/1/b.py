digit_spellings = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5, 
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "zero": 0,
}

def b(input: str) -> str:
    running_sum = 0
    for line in input.splitlines():
        first_digit = None
        last_digit = None
        for (idx, c) in enumerate(line):
            if c.isdigit():
                last_digit = int(c)
                if first_digit is None:
                    first_digit = int(c)
            for spelling, digit in digit_spellings.items():
                if line[idx:].startswith(spelling):
                    last_digit = digit
                    if first_digit is None:
                        first_digit = digit
        running_sum += first_digit * 10 + last_digit
    
    return str(running_sum)
