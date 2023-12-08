from itertools import groupby
from dataclasses import dataclass


def points(card: str, jokers_wild: bool = False) -> int:
    match card:
        case 'A': return 14
        case 'K': return 13
        case 'Q': return 12
        case 'J': return 1 if jokers_wild else 11
        case 'T': return 10
        case _: return int(card)


@dataclass
class Round:
    hand: list[str]
    bid: int
    jokers_wild: bool = False

    def grouped_hand(self) -> list[tuple[str, int]]:
        joker_count = self.hand.count('J')
        remaining_hand = [card for card in self.hand if card != 'J']
        if len(remaining_hand) == 0:
            return [('J', joker_count)]
        hand = sorted(remaining_hand, reverse=True)
        grouped_hand = list((card, len(list(cards))) for (card, cards) in groupby(hand))
        ordered_groups = sorted(grouped_hand, key=lambda x: x[1], reverse=True)
        # Add all the jokes to the card we already have the most of.
        updated_first_group = (ordered_groups[0][0], ordered_groups[0][1] + joker_count)
        ordered_groups[0] = updated_first_group
        return ordered_groups

    def type_score(self) -> int:
        grouped_hand = self.grouped_hand()
        if grouped_hand[0][1] == 5:
            # Five of a kind
            return 7
        if grouped_hand[0][1] == 4:
            # Four of a kind
            return 6
        if grouped_hand[0][1] == 3 and grouped_hand[1][1] == 2:
            # Full house
            return 5
        if grouped_hand[0][1] == 3:
            # Three of a kind
            return 4
        if grouped_hand[0][1] == 2 and grouped_hand[1][1] == 2:
            # Two pairs
            return 3
        if grouped_hand[0][1] == 2:
            # One pair
            return 2
        # High card
        return 1
    
    def wins_ties_over(self, other: 'Round') -> bool:
        for my_card, other_card in zip(self.hand, other.hand):
            my_card_score = points(my_card, jokers_wild=self.jokers_wild)
            other_card_score = points(other_card, jokers_wild=other.jokers_wild)
            if my_card_score > other_card_score:
                return True
            if my_card_score < other_card_score:
                return False
        raise RuntimeError("Tie")
    
    @classmethod
    def build_from_line(cls, line: str, jokers_wild: bool = False) -> 'Round':
        hand, bid = line.split()
        return cls(list(hand), int(bid), jokers_wild=jokers_wild)
    
    def __str__(self) -> str:
        return f"{self.hand} {self.bid}"
    
    @staticmethod
    def compare(a: 'Round', b: 'Round') -> int:
        a_tp_score = a.type_score()
        b_tp_score = b.type_score()
        if a_tp_score > b_tp_score:
            return 1
        elif a_tp_score < b_tp_score:
            return -1
        else:
            return 1 if a.wins_ties_over(b) else -1