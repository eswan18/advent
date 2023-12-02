from typing import Iterable
from dataclasses import dataclass

@dataclass
class Draw:
    RED: int
    BLUE: int
    GREEN: int

    @classmethod
    def from_str(cls, s: str) -> 'Draw':
        parts = s.split(', ')
        red = blue = green = 0
        for part in parts:
            part = part.strip()
            if part.endswith('red'):
                red = int(part.split(' ')[0])
            elif part.endswith('blue'):
                blue = int(part.split(' ')[0])
            elif part.endswith('green'):
                green = int(part.split(' ')[0])
        return cls(red, blue, green)

    @staticmethod
    def max_of(draws: Iterable['Draw']) -> 'Draw':
        max_draw = Draw(0, 0, 0)
        for draw in draws:
            if draw.RED > max_draw.RED:
                max_draw.RED = draw.RED
            if draw.BLUE > max_draw.BLUE:
                max_draw.BLUE = draw.BLUE
            if draw.GREEN > max_draw.GREEN:
                max_draw.GREEN = draw.GREEN
        return max_draw
    
    def power(self) -> int:
        return self.RED * self.BLUE * self.GREEN

@dataclass
class Game:
    id: int
    draws: list[Draw]

    @classmethod
    def from_str(cls, s: str) -> 'Game':
        id_str, draws = s.split(':')
        id = int(id_str.split(' ')[1])
        draws = [Draw.from_str(draw.strip()) for draw in draws.split('; ')]
        return cls(id, draws)
    
    def possible_from_draw(self, test: Draw):
        for draw in self.draws:
            if draw.RED > test.RED:
                return False
            if draw.BLUE > test.BLUE:
                return False
            if draw.GREEN > test.GREEN:
                return False
        return True

    def minimum_possible_draw(self) -> Draw:
        return Draw.max_of(self.draws)