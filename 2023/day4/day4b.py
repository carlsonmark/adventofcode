# Parse cards, winning numbers | card numbers
# Base points: 1, 2, 4, 8, 16, etc.
# ... plus points from N subsequent cards, where N is the number of correct numbers on this card

import dataclasses
from typing import List

example = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

# 4 +


@dataclasses.dataclass
class Card:
    number: int
    winning_numbers: List[int]
    card_numbers: List[int]
    copies: int=1

    @classmethod
    def from_str(cls, s: str):
        card_num_str, nums = s.split(':')
        number = int(card_num_str.split(' ')[-1])
        winning_numbers_str, card_numbers_str = nums.split('|')
        winning_numbers = [
            int(s) for s in winning_numbers_str.split(' ') if s
        ]
        card_numbers = [
            int(s) for s in card_numbers_str.split(' ') if s
        ]
        return Card(number, winning_numbers, card_numbers)

    def matches(self) -> int:
        matches = 0
        for winner in self.winning_numbers:
            if winner in self.card_numbers:
                matches += 1
        return matches

def solve(lines: str):
    cards = []
    for line in lines.splitlines():
        cards.append(Card.from_str(line))
    for i, card in enumerate(cards):
        matches = card.matches()
        for next_card in cards[i+1 : i+1+matches]:
            next_card.copies += card.copies
    total_copies = 0
    for card in cards:
        total_copies += card.copies
    print(f'{total_copies=}')

if __name__ == '__main__':
    solve(example)
    solve(open('day4input.txt').read())
