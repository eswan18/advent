from __future__ import annotations
from math import sqrt

from typing import Self
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def magnitude(self) -> float:
        return sqrt(self.x**2 + self.y**2)

    @classmethod
    def from_str(cls, s: str) -> Self:
        x_str, y_str = s.split(" ")
        x = int(x_str[2:-1])
        y = int(y_str[2:])
        return cls(x, y)

    def as_position(self) -> Position:
        return Position(self.x, self.y)

    def __add__(self, other: Self | int) -> Self:
        if isinstance(other, int):
            return self.__class__(self.x + other, self.y + other)
        if isinstance(other, self.__class__):
            return self.__class__(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __mul__(self, coef: int) -> Self:
        return Vector(self.x * coef, self.y * coef)

    def __rmul__(self, coef: int) -> Self:
        return Vector(self.x * coef, self.y * coef)


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def as_vector(self) -> Vector:
        return Vector(self.x, self.y)

    def factor(self, a: Vector, b: Vector) -> tuple[int, int]:
        """Find the coefficients of two component vectors or raise ValueError."""
        self_vec = self.as_vector()
        self_magnitude = self_vec.magnitude()
        # Using `a` costs 3 tokens and using `b` costs 1, so we want to use B as much as possible.
        # Start with the coef for `b` that get it as close as possible to the same magnitude as this position.
        b_magnitude = b.magnitude()
        b_coef = int(self_magnitude // b_magnitude)
        a_coef = 0 if b_coef > 0 else 1
        while b_coef > 0 or a_coef > 0:
            composed = a_coef * a + b_coef * b
            if composed == self_vec:
                return (a_coef, b_coef)
            if composed.x > self.x or composed.y > self.y:
                # If we've passed our target in either direction, then we've tried every
                # a_coef for this b_coef and we need to start again with a lower b_coef.
                b_coef -= 1
                a_coef = 0
            else:
                a_coef += 1
        raise ValueError("No whole number factors")

    def smart_factor(self, a: Vector, b: Vector) -> tuple[int, int]:
        "Find the coefs of two component vectors or raise ValueError. But smart."
        # I had to talk with my smart friend ChatGPT to learn about this method.
        determinant = a.x * b.y - b.x * a.y
        if determinant == 0:
            raise RuntimeError("linearly dependent")
        m = (b.y * self.x - b.x * self.y) / determinant
        n = (-a.y * self.x + a.x * self.y) / determinant
        result = (int(m), int(n))
        if result != (m, n):
            raise ValueError("non whole-number factors")
        return result


@dataclass
class Game:
    a: Vector
    b: Vector
    prize: Position

    @classmethod
    def from_str(cls, s: str, fix_conv_error: bool = False) -> Self:
        lines = s.splitlines()
        a = Vector.from_str(lines[0].removeprefix("Button A: "))
        b = Vector.from_str(lines[1].removeprefix("Button B: "))
        prize_vec = Vector.from_str(lines[2].removeprefix("Prize: "))
        if fix_conv_error:
            prize_vec += 10000000000000
        prize = prize_vec.as_position()
        return cls(a, b, prize)

    def cost(self) -> int:
        """How many tokens would it take to win this game? If it can be done."""
        a_coef, b_coef = self.prize.factor(self.a, self.b)
        return 3 * a_coef + b_coef

    def smart_cost(self) -> int:
        a_coef, b_coef = self.prize.smart_factor(self.a, self.b)
        return 3 * a_coef + b_coef
