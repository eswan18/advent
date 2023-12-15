from .platform import Platform


N = 1_000_000_000

def b(input: str) -> str:
    platform = Platform.build_from_str(input)
    hashes = {}
    cycles = 0
    while True:
        print(f'Cycle {cycles}...')
        platform.tilt_cyle()
        cycles += 1
        hash = platform.rounded_rock_hash()
        if hash in hashes:
            print(f'Cycle {cycles} matches cycle {hashes[hash]}')
            first_seen = hashes[hash]
            cycle_length = cycles - hashes[hash]
            break
        hashes[hash] = cycles
    print(f'First seen at {first_seen}, cycle length {cycle_length}')
    remaining_cycles = N - first_seen
    # We can skip even numbers of loops because they don't change the board.
    remaining_cycles %= cycle_length
    for i in range(remaining_cycles):
        platform.tilt_cyle()
    load = platform.load()
    return str(load)