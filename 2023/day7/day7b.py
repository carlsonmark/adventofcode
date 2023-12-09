from dataclasses import dataclass
from enum import IntEnum
from typing import List

example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

sorted_cards = list(reversed(['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']))
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
def is_one_pair(hand: str, joker_count: int) -> bool:
    for card in hand:
        if (hand.count(card) + joker_count) == 2:
            return True
    return False

def is_two_pair(hand: str, joker_count: int) -> bool:
    # 3 jokers at this point means it's 4 of a kind
    unique = list(set(hand))
    pair_count = 0
    for card in unique:
        if hand.count(card) == 2:
            pair_count += 1
    # Special case: 2 jokers + 1 pair at this point means it is a full house
    assert not (pair_count == 1 and joker_count == 2), f'{hand=}, {joker_count=}'
    # Special case: 2 jokers + 0 pairs means it's 2 pair
    if joker_count == 2 and pair_count == 0:
        return True
    # Special case: 1 joker plus a pair is 2 pair
    if joker_count == 1 and pair_count == 1:
        return True
    # No jokers, must be 2 natural pairs
    return pair_count == 2


def is_three_of_a_kind(hand: str, joker_count: int) -> bool:
    for card in hand:
        if (hand.count(card) + joker_count) == 3:
            return True
    return False

def is_full_house(hand: str, joker_count: int) -> bool:
    # Special case: 3 jokers at this point means it's a full house
    if joker_count == 3:
        return True
    # Special case: 2 jokers... if there are two other unique cards, then it's
    # a full house.
    unique = ''.join(set(hand))
    if joker_count == 2:
        if len(unique) == 2:
            return True
    # Special case: 1 joker... there has to be two natural pairs
    if joker_count == 1:
        counts = [hand.count(card) for card in unique]
        if counts.count(2) == 2:
            return True
    # No jokers
    if len(unique) == 2:
        counts = [hand.count(u) for u in unique]
        return 2 in counts and 3 in counts
    return False

def is_four_of_a_kind(hand: str, joker_count: int) -> bool:
    for card in hand:
        if (hand.count(card) + joker_count) == 4:
            return True
    return False

def is_five_of_a_kind(hand: str, joker_count: int) -> bool:
    if joker_count in (4, 5):
        return True
    return (joker_count + hand.count(hand[0])) == 5

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
        joker_count = self.sorted_cards.count('J')
        hand_no_jokers = self.sorted_cards.replace('J', '')
        if is_five_of_a_kind(hand_no_jokers, joker_count):
            handType = HandType.FiveOfAKind
        elif is_four_of_a_kind(hand_no_jokers, joker_count):
            handType = HandType.FourOfAKind
        elif is_full_house(hand_no_jokers, joker_count):
            handType = HandType.FullHouse
        elif is_three_of_a_kind(hand_no_jokers, joker_count):
            handType = HandType.ThreeOfAKind
        elif is_two_pair(hand_no_jokers, joker_count):
            handType = HandType.TwoPair
        elif is_one_pair(hand_no_jokers, joker_count):
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


