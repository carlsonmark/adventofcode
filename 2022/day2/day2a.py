ROCK = 'X'
PAPER = 'Y'
SCISSORS = 'Z'
ROCK_THEM = 'A'
PAPER_THEM = 'B'
SCISSORS_THEM = 'C'


def item_score(item):
    return {
        ROCK: 1,
        PAPER: 2,
        SCISSORS: 3
    }[item]


# Tricky: I thought it was (me, them)
def single_score(them, me):
    win_score = {
        ROCK: {
            ROCK_THEM: 3,
            PAPER_THEM: 0,
            SCISSORS_THEM: 6
        },
        PAPER: {
            ROCK_THEM: 6,
            PAPER_THEM: 3,
            SCISSORS_THEM: 0
        },
        SCISSORS: {
            ROCK_THEM: 0,
            PAPER_THEM: 6,
            SCISSORS_THEM: 3
        }
    }[me][them]
    score = win_score + item_score(me)
    # print(f'{me} {them} = {win_score} + {item_score(me)} = {score}')
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
