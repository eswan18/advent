from typing import Self
from dataclasses import dataclass
from collections import defaultdict
from itertools import combinations
import math

@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return self.__class__(
            x=self.x + other.x,
            y=self.y + other.y,
        )

    def __sub__(self, other: Self) -> Self:
        return self.__class__(
            x=self.x - other.x,
            y=self.y - other.y,
        )
    
    def reduce(self) -> Self:
        """Get a position with the smallest magnitude while still using whole number components."""
        gcd = math.gcd(self.x, self.y)
        return self.__class__(
            x=self.x // gcd,
            y=self.y // gcd,
        )


@dataclass
class AntennaMap:
    antennae: dict[str, list[Position]]
    width: int
    height: int

    @classmethod
    def from_string(cls, s: str) -> Self:
        antennae = defaultdict(list)
        for y, line in enumerate(s.splitlines()):
            for x, c in enumerate(line):
                if c != '.':
                    antennae[c].append(Position(x, y))
                width = x + 1
            height = y + 1
        return cls(
            antennae=dict(antennae),
            height=height,
            width=width,
        )
    
    def in_bounds(self, p: Position) -> bool:
        return 0 <= p.x < self.width and 0 <= p.y < self.height
    
    def antinodes_for_freq(self, freq: str) -> set[Position]:
        result = set()
        antennae = self.antennae[freq]
        for a, b in combinations(antennae, 2):
            a_to_b = b - a
            antinode_closer_to_b = b + a_to_b
            if self.in_bounds(antinode_closer_to_b):
                result.add(antinode_closer_to_b)
            antinode_closer_to_a = a - a_to_b
            if self.in_bounds(antinode_closer_to_a):
                result.add(antinode_closer_to_a)
        return result

    def antinodes(self) -> set[Position]:
        result = set()
        for freq in self.antennae.keys():
            result = result.union(self.antinodes_for_freq(freq))
        return result
    
    def antinodes_for_freq_part_b(self, freq: str) -> set[Position]:
        result = set()
        antennae = self.antennae[freq]
        for a, b in combinations(antennae, 2):
            a_to_b = (b - a).reduce()
            result.add(a)
            # Find all nodes "before" a.
            antinode = a
            while True:
                antinode = antinode - a_to_b
                if self.in_bounds(antinode):
                    result.add(antinode)
                else:
                    break
            # Find all nodes "after" a.
            antinode = a
            while True:
                antinode = antinode + a_to_b
                if self.in_bounds(antinode):
                    result.add(antinode)
                else:
                    break
        return result
    
    def antinodes_part_b(self) -> set[Position]:
        result = set()
        for freq in self.antennae.keys():
            result = result.union(self.antinodes_for_freq_part_b(freq))
        return result