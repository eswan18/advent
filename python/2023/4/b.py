from dataclasses import dataclass

from .parse import parse
from .card import Card


@dataclass
class CardAndCopies:
    card: Card
    copies: int


def b(input: str) -> str:
    cards = parse(input)
    cards_and_copies = [CardAndCopies(card, 1) for card in cards]
    cards_processed = 0
    while cards_and_copies:
        current = cards_and_copies.pop(0)
        cards_processed += current.copies
        matches = current.card.matches()
        for card in cards_and_copies[:matches]:
            card.copies += current.copies
    return str(cards_processed)