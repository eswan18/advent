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

def is_invalid_id(n: int) -> bool:
    as_str = str(n)
    str_len = len(as_str)
    for chunk_len in range(1, (str_len // 2) + 1):
        str_to_check = as_str
        if (str_len % chunk_len) != 0:
            continue
        chunk_to_match = str_to_check[0:chunk_len]
        remaining_str = str_to_check[chunk_len:]

        match = True
        while len(remaining_str) > 0:
            next_chunk = remaining_str[0:chunk_len]
            if next_chunk != chunk_to_match:
                match = False
                break
            remaining_str = remaining_str[chunk_len:]
        if match:
            return True

def b(input: str) -> str:
    ranges = input.strip().split(',')
    ranges = [Range.from_str(r) for r in ranges]

    invalid_ids_sum = 0
    for range in ranges:
        for number in range.numbers():
            if is_invalid_id(number):
                invalid_ids_sum += number
    return invalid_ids_sum
