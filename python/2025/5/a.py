from dataclasses import dataclass


@dataclass
class Range:
    start: int
    end: int

    def contains(self, n: int):
        return self.start <= n <= self.end

    @classmethod
    def from_str(cls, s: str) -> 'Range':
        parts = s.strip().split('-')
        if len(parts) != 2:
            raise ValueError('string must have one `-`')
        return cls(
            start=int(parts[0]),
            end=int(parts[1]),
        )


def a(input: str) -> str:
    parts = input.strip().split('\n\n')
    ranges = [Range.from_str(line) for line in parts[0].split('\n')]
    ingredient_ids = [int(line.strip()) for line in parts[1].split('\n')]

    n_fresh = 0
    for id in ingredient_ids:
        if id_is_in_ranges(id, ranges):
            n_fresh += 1
    return n_fresh
                


def id_is_in_ranges(id: int, ranges: list[Range]) -> bool:
    for range in ranges:
        if range.contains(id):
            return True
    return False
