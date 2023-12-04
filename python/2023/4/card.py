from dataclasses import dataclass

@dataclass
class Card:
    id: int
    winning_numbers: set[int]
    your_numbers: set[int]

    @classmethod
    def from_line(cls, line: str) -> 'Card':
        label, numbers = line.split(':')
        id = int(label.split(' ')[-1])
        winning_numbers, your_numbers = numbers.split(' | ')
        return cls(
            id=id,
            winning_numbers={int(n) for n in winning_numbers.split(' ') if len(n) > 0},
            your_numbers={int(n) for n in your_numbers.split(' ') if len(n) > 0},
        )
    
    def matches(self) -> int:
        return len(self.winning_numbers & self.your_numbers)
    
    def points(self) -> int:
        matches = self.matches()
        if matches == 0:
            return 0
        return 2 ** (matches - 1)