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

    def size(self) -> int:
        return self.end - self.start + 1


def b(input: str) -> str:
    parts = input.strip().split('\n\n')
    # Sort by the start of each range so we can merge ranges.
    ranges = sorted(
        (Range.from_str(line) for line in parts[0].split('\n')),
        key=lambda r: (r.start, r.end),
    )
    while True:
        found_merge = merge_ranges(ranges)
        if not found_merge:
            break

    return sum(r.size() for r in ranges)


def merge_ranges(ranges: list[Range]) -> bool:
    for i in range(len(ranges)-1):
        if ranges[i].end >= ranges[i+1].start:
            ranges[i].end = max(ranges[i].end, ranges[i+1].end)
            # Remove the range we've now "absorbed"
            ranges.pop(i+1)
            return True
    return False
