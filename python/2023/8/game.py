from dataclasses import dataclass
from enum import StrEnum


class Instruction(StrEnum):
    R = 'R'
    L = 'L'


@dataclass
class Node:
    name: str
    left: str
    right: str

    @classmethod
    def build_from_line(cls, line: str) -> 'Node':
        name, left_right = line.split(" = ")
        left, right = left_right.strip("()").split(", ")
        return cls(name, left, right)


@dataclass
class Game:
    instructions: list[Instruction]
    nodes: dict[str, Node]

    @classmethod
    def build_from_str(cls, input: str) -> 'Game':
        lines = input.splitlines()
        instructions = [Instruction(c) for c in lines[0]]

        node_list = [Node.build_from_line(line) for line in lines[2:]]
        nodes = {node.name: node for node in node_list}
        return cls(instructions, nodes)
    

    def play(self) -> int:
        state = GameState("AAA", 0)
        while state.node != "ZZZ":
            instruction = self.instructions[state.instr_idx % len(self.instructions)]
            match instruction:
                case Instruction.R:
                    state = GameState(self.nodes[state.node].right, state.instr_idx + 1)
                case Instruction.L:
                    state = GameState(self.nodes[state.node].left, state.instr_idx + 1) 
        return state.instr_idx


@dataclass
class GameState:
    node: str
    instr_idx: int