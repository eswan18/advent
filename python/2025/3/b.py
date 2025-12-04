from dataclasses import dataclass

DIGITS_NEEDED = 12

@dataclass
class Bank:
    batteries: list[int]

    @classmethod
    def from_str(cls, s: str) -> 'Bank':
        return cls(batteries=[int(c) for c in s.strip()])
    
    def largest_joltage(self) -> int:
        digits_chosen = []
        indexes_chosen = []
        # Select the largest
        while len(digits_chosen) < DIGITS_NEEDED:
            digits_still_needed = DIGITS_NEEDED - len(digits_chosen)

            start = indexes_chosen[-1] + 1 if indexes_chosen else 0
            end = -(digits_still_needed - 1)
            if end == 0:
                end = None
            digit_options = self.batteries[start:end]
            idx, val = max(enumerate(digit_options), key=lambda x: x[1])
            idx += start

            digits_chosen.append(val)
            indexes_chosen.append(idx)
        result = int(''.join(str(i) for i in digits_chosen))
        return result

def b(input: str) -> str:
    banks = [Bank.from_str(line) for line in input.splitlines()]
    return  sum(bank.largest_joltage() for bank in banks)
