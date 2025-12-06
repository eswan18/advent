import functools
from typing import Literal, cast, Never
from dataclasses import dataclass

type Operator = Literal['*', '+']

@dataclass
class Expression:
    numbers: tuple[int]
    operator: Operator

    def result(self) -> int:
        match self.operator:
            case '+':
                return sum(self.numbers)
            case '*':
                return functools.reduce(lambda x, y: x * y, self.numbers, 1)
            case _:
                Never


def a(input: str) -> str:
    lines = input.strip().splitlines()
    *lines, op_line = lines
    numbers = [[int(s) for s in line.strip().split(' ') if s.isdigit()] for line in lines]
    numbers = zip(*numbers)
    ops: list[Operator] = [cast(Operator, s) for s in op_line.strip().split(' ') if len(s) > 0]
    exprs = [Expression(n, op) for (n, op) in zip(numbers, ops)]
    results = [e.result() for e in exprs]
    return str(sum(results))