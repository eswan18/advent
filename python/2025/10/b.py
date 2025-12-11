from typing import Self, Iterable
from dataclasses import dataclass
from itertools import combinations, combinations_with_replacement

@dataclass(frozen=True)
class Vector:
    v: tuple[int, ...]

    @classmethod
    def new(cls, value: Iterable[int]) -> Self:
        return cls(v=tuple(value))
    
    @classmethod
    def empty(cls, length: int) -> Self:
        return cls(v=tuple(0 for _ in range(length)))
    
    @classmethod
    def from_indices(cls, indices: Iterable[int], length: int) -> Self:
        return cls.new(1 if idx in indices else 0 for idx in range(length))
    
    @classmethod
    def from_csv(cls, s: str, length: int) -> Self:
        values = [int(v) for v in s.split(',')]
        return cls.from_indices(indices=values, length=length)
    
    def __add__(self, other: Self) -> Self:
        if not isinstance(other, Vector):
            return NotImplemented
        if len(self) != len(other):
            raise ValueError("Can't add vectors of different lengths")
        values = tuple(x + y for (x, y) in zip(self.v, other.v))
        return self.__class__(values)
    
    def __mod__(self, m: int) -> Self:
        return self.__class__(tuple(v % m for v in self.v))
    
    def __len__(self) -> int:
        return len(self.v)
    
    def __str__(self) -> str:
        return f"[{', '.join(str(v) for v in self.v)}]"


@dataclass(frozen=True)
class Spec:
    indicators: Vector
    buttons: list[Vector]
    joltage: Vector

    @classmethod
    def from_line(cls, l: str) -> Self:
        indicator_str, *button_strs, joltage_str = l.split(' ')
        indicator_str = indicator_str.removeprefix('[').removesuffix(']')
        indicators = Vector.new((1 if c == '#' else 0) for c in indicator_str)
        button_strs = (b.removeprefix('(').removesuffix(')') for b in button_strs)
        buttons = [Vector.from_csv(b, length=len(indicators)) for b in button_strs]
        joltage_str = joltage_str.removeprefix('{').removesuffix('}')
        joltage = Vector.new(int(i) for i in joltage_str.split(','))
        return cls(
            indicators=indicators,
            buttons=buttons,
            joltage=joltage,
        )
    
    def fewest_presses(self) -> int:
        n_presses = 1
        while True:
            for buttons in combinations_with_replacement(self.buttons, n_presses):
                v = Vector.empty(len(self.indicators))
                for b in buttons:
                    v += b
                if v == self.joltage:
                    print(f'done! presses: {n_presses}')
                    return n_presses
            # Restart the loop, but try larger combinations.
            n_presses += 1 

def b(input: str) -> str:
    specs = [Spec.from_line(line) for line in input.splitlines()]
    n_presses = [s.fewest_presses() for s in specs]
    return str(sum(n_presses))