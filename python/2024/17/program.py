from __future__ import annotations
from typing import Literal, Self
from dataclasses import dataclass


@dataclass
class State:
    ip: int  # instruction pointer
    a: int
    b: int
    c: int

    @classmethod
    def from_str(cls, s: str) -> Self:
        lines = s.splitlines()
        a = int(lines[0].split(" ")[-1])
        b = int(lines[1].split(" ")[-1])
        c = int(lines[2].split(" ")[-1])
        return cls(ip=0, a=a, b=b, c=c)

    def eval_instruction(self, instr: Instruction) -> int | None:
        match instr:
            case Instruction("adv", combo_op):
                numerator = self.a
                denominator = 2 ** combo_op.value(self)
                self.a = numerator // denominator
                self.ip += 1
            case Instruction("bxl", op):
                self.b = self.b ^ op
                self.ip += 1
            case Instruction("bst", combo_op):
                self.b = combo_op.value(self) % 8
                self.ip += 1
            case Instruction("jnz", op):
                if self.a != 0:
                    self.ip = op // 2
                else:
                    self.ip += 1
            case Instruction("bxc", _):
                self.b = self.b ^ self.c
                self.ip += 1
            case Instruction("out", combo_op):
                value = combo_op.value(self) % 8
                self.ip += 1
                return value
            case Instruction("bdv", combo_op):
                numerator = self.a
                denominator = 2 ** combo_op.value(self)
                self.b = numerator // denominator
                self.ip += 1
            case Instruction("cdv", combo_op):
                numerator = self.a
                denominator = 2 ** combo_op.value(self)
                self.c = numerator // denominator
                self.ip += 1
            case _:
                raise ValueError(f"Unexpected instruction {instr}")

    def run(self, instructions: list[Instruction]) -> list[int]:
        output: list[int] = []
        while self.ip < len(instructions):
            result = self.eval_instruction(instructions[self.ip])
            if result is not None:
                output.append(result)
        return output


@dataclass(frozen=True)
class ComboOperand:
    operand: int

    def value(self, state: State) -> int:
        if self.operand <= 3:
            return self.operand
        if self.operand == 4:
            return state.a
        if self.operand == 5:
            return state.b
        if self.operand == 6:
            return state.c
        raise ValueError(f"Unexpected ComboOperand: {self.operand}")


OpCode = Literal["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]


@dataclass(frozen=True)
class Instruction:
    code: OpCode
    operand: int | ComboOperand | None

    @classmethod
    def from_ints(cls, operator: int, operand: int) -> Self:
        match operator:
            case 0:
                return cls("adv", ComboOperand(operand))
            case 1:
                return cls("bxl", operand)
            case 2:
                return cls("bst", ComboOperand(operand))
            case 3:
                return cls("jnz", operand)
            case 4:
                return cls("bxc", None)
            case 5:
                return cls("out", ComboOperand(operand))
            case 6:
                return cls("bdv", ComboOperand(operand))
            case 7:
                return cls("cdv", ComboOperand(operand))
            case _:
                raise ValueError(f"Unexpected operator {operator}")

    @classmethod
    def from_str(cls, s: str) -> list[Self]:
        s = s.removeprefix("Program: ")
        raw = [int(i) for i in s.split(",")]
        instructions = [
            Instruction.from_ints(raw[idx], raw[idx + 1])
            for idx in range(0, len(raw), 2)
        ]
        return instructions


def test_instructions():
    state = State(ip=0, a=0, b=0, c=9)
    state.eval_instruction(Instruction.from_ints(2, 6))
    assert state.ip == 1
    assert state.a == 0
    assert state.b == 1
    assert state.c == 9

    state = State(ip=0, a=10, b=0, c=0)
    result = state.run(Instruction.from_str("5,0,5,1,5,4"))
    assert result == [0, 1, 2]

    state = State(ip=0, a=2024, b=0, c=0)
    result = state.run(Instruction.from_str("0,1,5,4,3,0"))
    assert state.a == 0
    assert result == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]

    state = State(ip=0, a=0, b=29, c=0)
    result = state.run(Instruction.from_str("1,7"))
    assert state.a == 0
    assert state.b == 26
    assert state.c == 0

    state = State(ip=0, a=0, b=2024, c=43690)
    result = state.run(Instruction.from_str("4,0"))
    assert state.a == 0
    assert state.b == 44354
    assert state.c == 43690