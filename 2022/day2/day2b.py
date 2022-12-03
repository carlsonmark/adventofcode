LOSE = 'X'
DRAW = 'Y'
WIN = 'Z'
ROCK = 'A'
PAPER = 'B'
SCISSORS = 'C'


def item_score(item):
    return {
        ROCK: 1,
        PAPER: 2,
        SCISSORS: 3
    }[item]


def outcome(them, me):
    return {
        ROCK: {
            ROCK: DRAW,
            PAPER: LOSE,
            SCISSORS: WIN
        },
        PAPER: {
            ROCK: WIN,
            PAPER: DRAW,
            SCISSORS: LOSE
        },
        SCISSORS: {
            ROCK: LOSE,
            PAPER: WIN,
            SCISSORS: DRAW
        }
    }[me][them]


def my_item(them, goal):
    for item in (ROCK, PAPER, SCISSORS):
        if outcome(them, item) == goal:
            return item


# Tricky: I thought it was (me, them)
def single_score(them, goal):
    me = my_item(them, goal)
    win_score = {
        WIN: 6,
        DRAW: 3,
        LOSE: 0
    }[outcome(them, me)]
    score = win_score + item_score(me)
    return score


test_data = """A Y
B X
C Z"""

total_score = 0
for line in test_data.split('\n'):
    total_score += single_score(*line.split(' '))

print(f'Test: {total_score=}')

total_score = 0
for line in open('day2-input.txt').readlines():
    total_score += single_score(*line.strip('\n').split(' '))
print(f'Test: {total_score=}')
