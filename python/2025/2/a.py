from typing import Iterator
from dataclasses import dataclass

@dataclass
class Range:
    start: int
    end: int

    def numbers(self) -> Iterator[int]:
        current = self.start
        while current <= self.end:
            yield current
            current += 1

    @classmethod
    def from_str(cls, s: str) -> 'Range':
        components = s.strip().split('-')
        assert len(components) == 2
        start = int(components[0])
        end = int(components[1])
        return cls(start, end)

def a(input: str) -> str:
    ranges = input.strip().split(',')
    ranges = [Range.from_str(r) for r in ranges]

    invalid_ids_sum = 0
    for range in ranges:
        for number in range.numbers():
            as_str = str(number)
            half_point = len(as_str) // 2
            if as_str[:half_point] == as_str[half_point:]:
                invalid_ids_sum += number
    return invalid_ids_sum
