from .program import State, Instruction


def a(input: str) -> str:
    register_str, instr_str = input.split("\n\n")
    state = State.from_str(register_str)
    instructions = Instruction.from_str(instr_str)
    return ','.join(str(i) for i in state.run(instructions))
