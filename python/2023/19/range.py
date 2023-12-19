from dataclasses import dataclass


@dataclass
class Range:
    """An inclusive range of integers."""
    start: int
    end: int

    def __len__(self) -> int:
        return self.end - self.start + 1