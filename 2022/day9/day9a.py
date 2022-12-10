# Notes:
# Moving an extremely short rope on a 2D grid
# Head/tail must always be touching
# Input is direction the head travels
# Tail will not always move into the head's position, e.g. when cornering
# Output is how many unique spots the tail has been

import numpy as np

test_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

direction_step = dict(R=(1, 0), L=(-1, 0), U=(0, 1), D=(0, -1))


def calc_tail_pos(old_head_pos, new_head_pos, tail_pos):
    new_x, new_y = new_head_pos
    tail_x, tail_y = tail_pos
    if abs(new_x - tail_x) >= 2:
        tail_pos = old_head_pos
    elif abs(new_y - tail_y) >= 2:
        tail_pos = old_head_pos
    return tail_pos


def print_locations(locations):
    max_x = 0
    max_y = 0
    for location in locations:
        x, y = location
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    a = np.zeros((max_y+1, max_x+1), dtype=int)
    for location in locations:
        x, y = location
        a[y, x] = 1
    print(a[::-1])


def parse_input(moves):
    head_x = 0
    head_y = 0
    tail_x = 0
    tail_y = 0
    tail_location_list = {(tail_x, tail_y)}
    for line in moves.splitlines(keepends=False):
        direction, amount_str = line.split(' ')
        amount = int(amount_str)
        for move in range(amount):
            x_step, y_step = direction_step[direction]
            new_head_x = head_x + x_step
            new_head_y = head_y + y_step
            tail_x, tail_y = calc_tail_pos((head_x, head_y), (new_head_x, new_head_y), (tail_x, tail_y))
            print(tail_x, tail_y)
            head_x = new_head_x
            head_y = new_head_y
            tail_location_list.add((tail_x, tail_y))
            # print_locations(tail_location_list)
    return tail_location_list

tail_location_list = parse_input(test_input)
print(f'{tail_location_list=}')
print(f'{len(tail_location_list)=}')

tail_location_list = parse_input(open('day9-input.txt').read())
# print(f'{tail_location_list=}')
print(f'{len(tail_location_list)=}')
