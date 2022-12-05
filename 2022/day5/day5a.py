# Notes:
# Crane moving crates
# It can only move one crate at a time
# Multiple moves may be performed per line, and will result in the stack
# being upside-down when moved.
# The answer is the letters of the crates on the top of each stack.
import dataclasses

test_input_a = """    [D]    
[N] [C]    
[Z] [M] [P]
"""

test_input_b = """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


def parse_stacks(s):
    # When saving in pycharm, the space at the end of the line is removed,
    # so check the last line for the number of stacks
    last_line = next(reversed(s.splitlines(keepends=False)))
    stacks = [[] for _ in range(len(last_line) // 4 + 1)]
    # Iterate lines in reverse order so bottom is at the start
    for line in reversed(s.splitlines(keepends=False)):
        for i in range(len(line) // 4 + 1):
            crate = line[i*4+1]
            if crate != ' ':
                stacks[i].append(crate)
    return stacks


@dataclasses.dataclass
class Move:
    how_many: int
    from_where: int
    to_where: int


def parse_moves(s):
    moves = []
    for line in s.splitlines(keepends=False):
        line = line.replace('move ', '').replace('from ', '').replace('to ', '')
        split = line.split(' ')
        moves.append(Move(how_many=int(split[0]),
                          from_where=int(split[1]) - 1,
                          to_where=int(split[2]) - 1))
    return moves


def execute_move(stacks, move):
    from_stack = stacks[move.from_where]
    to_stack = stacks[move.to_where]
    for count in range(move.how_many):
        to_stack.append(from_stack.pop())
    return stacks


def execute_moves(stacks, moves):
    for move in moves:
        stacks = execute_move(stacks, move)
    return stacks


stacks = parse_stacks(test_input_a)
moves = parse_moves(test_input_b)
stacks = execute_moves(stacks, moves)
solution = ''
for stack in stacks:
    solution += stack[-1]
print(f'{solution=}')


stacks = parse_stacks(open('day5-input-a.txt').read())
moves = parse_moves(open('day5-input-b.txt').read())
stacks = execute_moves(stacks, moves)
solution = ''
for stack in stacks:
    solution += stack[-1]
print(f'{solution=}')
