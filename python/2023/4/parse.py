from .card import Card

def parse(input: str) -> list[Card]:
    cards = [Card.from_line(line) for line in input.splitlines()]
    return cards