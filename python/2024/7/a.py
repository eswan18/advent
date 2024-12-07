from typing import Self, Literal, TypeAlias
from dataclasses import dataclass

Operator: TypeAlias = Literal['add', 'mul']

@dataclass
class Equation:
    result: int
    operators: list[Operator]
    operands: list[int]

    @classmethod
    def from_str(cls, s: str) -> Self:
        result_str, operand_str = s.split(':', 1)
        result = int(result_str)
        operands = [int(o) for o in operand_str.strip().split(' ')]
        return cls(result=result, operands=operands, operators=[])
    
    def is_complete(self) -> bool:
        '''Does this equation have enough operators defined?'''
        if len(self.operators) + 1 < len(self.operands):
            return False
        return True
    
    def is_valid(self) -> bool:
        '''Does this equation actually check out?'''
        if not self.is_complete():
            raise RuntimeError("Can't check validity of imcomplete equation")
        lhs = self.result
        rhs = self.operands[0]
        i = 1
        for i in range(1, len(self.operands)):
            match self.operators[i-1]:
                case 'mul':
                    rhs *= self.operands[i]
                case 'add':
                    rhs += self.operands[i]
        return lhs == rhs
        

def a(input: str) -> str:
    lines = [Equation.from_str(s) for s in input.splitlines()]
    eq = Equation(result=100, operands=[4, 2, 9, 28], operators=['mul', 'mul', 'add'])
    print(eq.is_complete())
    print(eq.is_valid())
    print(lines[0])