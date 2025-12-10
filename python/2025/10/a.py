from typing import Self
from dataclasses import dataclass

@dataclass(frozen=True)
class Button:
    indicators: tuple[int, ...]

    @classmethod
    def from_str(cls, s: str) -> Self:
        s = s.removeprefix('(').removesuffix(')')
        return cls(tuple(int(n) for n in s.split(',')))

@dataclass(frozen=True)
class Spec:
    indicators: tuple[bool, ...]
    buttons: list[Button]
    joltage: str

    @classmethod
    def from_line(cls, l: str) -> Self:
        indicator_str, *button_strs, joltage = l.split(' ')
        indicator_str = indicator_str.removeprefix('[').removesuffix(']')
        indicators = tuple(c == '#' for c in indicator_str)
        buttons = [Button.from_str(b) for b in button_strs]
        return cls(
            indicators=indicators,
            buttons=buttons,
            joltage=joltage,
        )

def a(input: str) -> str:
    specs = [Spec.from_line(line) for line in input.splitlines()]
    for s in specs:
        print(s)