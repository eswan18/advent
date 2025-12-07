import functools
from typing import Literal, Never, Self
from dataclasses import dataclass, field
from itertools import zip_longest

type Operator = Literal['*', '+']


@dataclass
class ColumnSet:
    """A group of columns that represent one expression."""
    cols: list[list[str]] = field(default_factory=list)

@dataclass
class Expression:
    numbers: list[int]
    operator: Operator

    @classmethod
    def from_column_set(cls, col_set: ColumnSet) -> Self:
        operator = col_set.cols[0].pop()
        if operator not in ('*', '+'):
            raise RuntimeError
        # Turn each column into a number
        numbers = [int(''.join(c for c in col if c is not None).strip()) for col in col_set.cols]
        return cls(numbers=numbers, operator=operator)
    
    def result(self) -> int:
        match self.operator:
            case '*':
                return functools.reduce(lambda x, y: x * y, self.numbers, 1)
            case '+':
                return sum(self.numbers)
            case _:
                Never



def b(input: str) -> str:
    lines = input.strip().splitlines()
    line_chars = [[s for s in line] for line in lines]
    col_chars: list[tuple[str]] = list(zip_longest(*line_chars))
    
    # Loop over the columns
    col_sets: list[ColumnSet] = []
    current_col_set = ColumnSet()
    while col_chars:
        column = col_chars.pop(0)
        # If all the characters are blanks, we've finished a column set
        if all(c == ' ' for c in column):
            col_sets.append(current_col_set)
            current_col_set = ColumnSet()
            continue
            
        current_col_set.cols.append(list(column))
    col_sets.append(current_col_set)

    exprs = [Expression.from_column_set(c) for c in col_sets]
    results = [e.result() for e in exprs]
    return str(sum(results))