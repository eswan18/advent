from .instruction import Instruction
from .path import Path


def a(input: str) -> str:
    instructions = [Instruction.build_from_line(line) for line in input.splitlines()]
    path = Path()
    for i in instructions:
        path.do(i)
    return str(path.calculate_area())