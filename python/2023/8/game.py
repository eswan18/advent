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
    end_node_type: str = "ZZZ"

    @classmethod
    def build_from_str(cls, input: str, end_node_type: str = "ZZZ") -> 'Game':
        lines = input.splitlines()
        instructions = [Instruction(c) for c in lines[0]]

        node_list = [Node.build_from_line(line) for line in lines[2:]]
        nodes = {node.name: node for node in node_list}
        return cls(instructions, nodes, end_node_type=end_node_type)
    

    def play(self) -> int:
        return self.distance_to_end("AAA")
    
    def at_end(self, node: str) -> bool:
        if self.end_node_type == "ZZZ":
            return node == "ZZZ"
        else:
            return node.endswith("Z")
    
    def ghost_play(self) -> int:
        # Find all nodes ending with A
        start_nodes = [name for name in self.nodes.keys() if name.endswith("A")]
        state = GhostGameState(start_nodes, 0)
        # Play until all nodes end with Z.
        while not all(self.at_end(node) for node in state.nodes):
            instruction = self.instructions[state.instr_idx % len(self.instructions)]
            match instruction:
                case Instruction.R:
                    next_nodes = [self.nodes[node].right for node in state.nodes]
                    state = GhostGameState(next_nodes, state.instr_idx + 1)
                case Instruction.L:
                    next_nodes = [self.nodes[node].left for node in state.nodes]
                    state = GhostGameState(next_nodes, state.instr_idx + 1)
        return state.instr_idx
    
    def distance_to_end(self, node: str) -> int:
        state = GameState(node, 0)
        while not self.at_end(state.node):
            instruction = self.instructions[state.instr_idx % len(self.instructions)]
            match instruction:
                case Instruction.R:
                    state = GameState(self.nodes[state.node].right, state.instr_idx + 1)
                case Instruction.L:
                    state = GameState(self.nodes[state.node].left, state.instr_idx + 1) 
        return state.instr_idx
    
    def build_distances(self) -> dict[str, int]:
        distances = {}
        for node in self.nodes.keys():
            print(f'building node distances for {node}')
            distances[node] = self.distance_to_end(node)
        print(distances)
        return distances


@dataclass
class GameState:
    node: str
    instr_idx: int

@dataclass
class GhostGameState:
    nodes: list[str]
    instr_idx: int