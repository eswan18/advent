from multiprocessing import Pool
from functools import partial

from .program import State, Instruction


def b(input: str) -> str:
    register_str, instr_str = input.split("\n\n")
    state = State.from_str(register_str)
    instructions = Instruction.from_str(instr_str)
    instr_str = instr_str.removeprefix("Program: ").strip()

    n_cpus = 8
    n_iter = 100_000_000_000
    per_core = n_iter // n_cpus
    # starts = [per_core * i for i in range(n_cpus)]
    # tried this up to 57225000000 and still no luck.
    result =check_quine(start=26600000, length=n_iter, state=state, instructions=instructions, check_against=[
            int(i) for i in instr_str.removeprefix("Program: ").strip().split(",")
        ])
    return str(result)
    #check_quine_bound = partial(
        #check_quine,
        #length=per_core,
        #state=state,
        #instructions=instructions,
        #check_against=[
        #    int(i) for i in instr_str.removeprefix("Program: ").strip().split(",")
        #],
    #)
    #with Pool(n_cpus) as pool:
        #for result in pool.imap_unordered(check_quine_bound, starts):
            #print("one of them is done!", result)
            #if result is not None:
                #return str(result)


def check_quine(
    start: int,
    length: int,
    state: State,
    instructions: list[Instruction],
    check_against: list[int],
) -> int | None:
    for i in range(length):
        check_state = State(ip=0, a=start + i, b=state.b, c=state.c)
        if i % 100_000 == 0:
            print(i)
        ok = True
        result = check_state.run(instructions)
        for expected in check_against:
            try:
                actual = next(result)
            except StopIteration:
                ok = False
                break
            if actual != expected:
                ok = False
                break
        if ok:
            return start + i
    return None
