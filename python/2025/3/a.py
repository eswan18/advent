from dataclasses import dataclass

@dataclass
class Bank:
    batteries: list[int]

    @classmethod
    def from_str(cls, s: str) -> 'Bank':
        return cls(batteries=[int(c) for c in s.strip()])
    
    def largest_joltage(self) -> int:
        # Just look for the first 9, or if not a 9 then an 8, etc.
        # It seems like a stupid idea but saves us from sorting the list.
        first_digit = 9
        first_digit_idx = -1
        found = False
        while not found:
            # Go through each position in the string looking for the digit.
            for idx, digit in enumerate(self.batteries[:-1]):
                if digit == first_digit:
                    first_digit_idx = idx
                    found = True
                    break
            if found:
                break
            first_digit -=1

        # Now find the second digit by just getting the highest digit to the right of
        # the one we found.
        second_digit = max(self.batteries[first_digit_idx+1:])

        return 10 * first_digit + second_digit

def a(input: str) -> str:
    banks = [Bank.from_str(line) for line in input.splitlines()]
    return  sum(bank.largest_joltage() for bank in banks)
