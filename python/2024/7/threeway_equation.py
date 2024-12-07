from typing import Self, Literal, TypeAlias, Iterator
from dataclasses import dataclass

Operator: TypeAlias = Literal['add', 'mul', 'concat']

@dataclass(frozen=True)
class ThreewayEquation:
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
            raise RuntimeError("Can't check validity of incomplete equation")
        lhs = self.result
        rhs = self.operands[0]
        i = 1
        for i in range(1, len(self.operands)):
            match self.operators[i-1]:
                case 'mul':
                    rhs *= self.operands[i]
                case 'add':
                    rhs += self.operands[i]
                case 'concat':
                    rhs = int(str(rhs) + str(self.operands[i]))
        return lhs == rhs

    def all_possible_complete_states(self) -> Iterator[Self]:
        if self.is_complete():
            yield self
            return 
        # Recursively traverse down in the case of add and mul separately.
        yield from self.__class__(
            result=self.result,
            operands=[o for o in self.operands],
            operators=[o for o in self.operators] + ['add'],
        ).all_possible_complete_states()
        yield from self.__class__(
            result=self.result,
            operands=[o for o in self.operands],
            operators=[o for o in self.operators] + ['mul'],
        ).all_possible_complete_states()
        yield from self.__class__(
            result=self.result,
            operands=[o for o in self.operands],
            operators=[o for o in self.operators] + ['concat'],
        ).all_possible_complete_states()
    
    def has_solution(self) -> bool:
        for state in self.all_possible_complete_states():
            if state.is_valid():
                return True
        return False