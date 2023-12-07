from .parse import parse


def b(input: str) -> str:
    game = parse(input, seeds_type='range')
    # Start at the lowest destination range and test every point until finding one that can be translated backward.
    dest_ranges = game.destination_ranges()
    for dest in range(0, dest_ranges[-1][1] + 1):
        if dest % 100_000 == 0:
            print(f'Destination: {dest}')
        source = game.backward_translate(dest)
        if game.has_seed(source):
            return str(dest)
    return 'No solution found'