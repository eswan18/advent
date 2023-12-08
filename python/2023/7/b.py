from functools import cmp_to_key

from .round import Round


def b(input: str) -> str:
    rounds = [Round.build_from_line(line, jokers_wild=True) for line in input.splitlines()]
    # Order the rounds by their type_score
    sorted_rounds = sorted(rounds, key=cmp_to_key(Round.compare))
    winnings = 0
    for rank, round in enumerate(sorted_rounds, start=1):
        score = rank * round.bid
        winnings += score
    return str(winnings)