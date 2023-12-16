from .hash import Instruction, State


def b(input: str) -> str:
    pieces = input.strip().split(",")
    instrs = list(Instruction.build_from_string(piece) for piece in pieces)
    state = State()
    for i in instrs:
        state.execute(i)
    return str(state.focusing_power())