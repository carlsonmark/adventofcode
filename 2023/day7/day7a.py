from dataclasses import dataclass
from enum import IntEnum
from typing import List

example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

sorted_cards = list(reversed(['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']))
def win_lose_draw(a: str, b: str):
    """
    Returns > 0 if a > b
    Returns < 0 if a < b
    Returns 0 if a == b
    """
    return sorted_cards.index(a) - sorted_cards.index(b)


class HandType(IntEnum):
    HighCard = 0
    OnePair = 1
    TwoPair = 2
    ThreeOfAKind = 3
    FullHouse = 4
    FourOfAKind = 5
    FiveOfAKind = 6

# Note: These must be run in order from best hand to worst
def is_one_pair(hand: str) -> bool:
    unique = list(set(hand))
    for card in unique:
        if hand.count(card) == 2:
            return True
    return False

def is_two_pair(hand: str) -> bool:
    unique = list(set(hand))
    pair_count = 0
    for card in unique:
        if hand.count(card) == 2:
            pair_count += 1
    return pair_count == 2

def is_three_of_a_kind(hand: str) -> bool:
    unique = set(hand)
    for card in unique:
        if hand.count(card) == 3:
            return True
    return False

def is_full_house(hand: str) -> bool:
    unique = ''.join(set(hand))
    if len(unique) == 2:
        counts = [hand.count(u) for u in unique]
        return 2 in counts and 3 in counts
    return False

def is_four_of_a_kind(hand: str) -> bool:
    return hand.count(hand[0]) == 4 or hand.count(hand[1]) == 4

def is_five_of_a_kind(hand: str) -> bool:
    return hand.count(hand[0]) == 5

@dataclass
class Hand:
    hand: str
    bid: int
    handType: HandType = HandType.HighCard
    sorted_cards: str = ''

    def __post_init__(self):
        self.sorted_cards = ''.join(sorted([s for s in self.hand]))
        self.handType = self.calculate_hand_type()
        return

    @classmethod
    def from_str(cls, line: str):
        hand, bid_str = line.split(' ')
        return Hand(hand, int(bid_str))

    def calculate_hand_type(self):
        handType = HandType.HighCard
        if is_five_of_a_kind(self.sorted_cards):
            handType = HandType.FiveOfAKind
        elif is_four_of_a_kind(self.sorted_cards):
            handType = HandType.FourOfAKind
        elif is_full_house(self.sorted_cards):
            handType = HandType.FullHouse
        elif is_three_of_a_kind(self.sorted_cards):
            handType = HandType.ThreeOfAKind
        elif is_two_pair(self.sorted_cards):
            handType = HandType.TwoPair
        elif is_one_pair(self.sorted_cards):
            handType = HandType.OnePair
        return handType

    def __lt__(self, other):
        if self.handType < other.handType:
            return True
        elif self.handType > other.handType:
            return False
        # They are the same type, check the cards in order
        for this_card, that_card in zip(iter(self.hand), iter(other.hand)):
            wld = win_lose_draw(this_card, that_card)
            if wld > 0:
                return False
            if wld < 0:
                return True
        assert False, f'{self.hand} ??? {other.hand}'

def parse(s: str) -> List[Hand]:
    hands = [Hand.from_str(line) for line in s.splitlines()]
    return hands

def solve(s: str):
    hands = parse(s)
    winnings = 0
    for i, hand in enumerate(sorted(hands)):
        rank = i + 1
        winnings += rank * hand.bid
        print(rank, hand)
    print(f'{winnings=}')

if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())

# 249455514 too low
# 249941600 too high
