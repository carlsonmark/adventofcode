# Notes:
# Longer rope now with 9 non-head positions
# Keep track of the tail (the 9th)

import numpy as np
np.set_printoptions(edgeitems=30, linewidth=100000)

test_input = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""


direction_step = dict(R=(1, 0), L=(-1, 0), U=(0, 1), D=(0, -1))


def calc_tail_pos(new_head_pos, tail_pos):
    new_x, new_y = new_head_pos
    tail_x, tail_y = tail_pos
    if abs(new_x - tail_x) >= 2:
        tail_x += np.sign(new_x - tail_x)
        if abs(new_y - tail_y) >= 1:
            tail_y += np.sign(new_y - tail_y)
    elif abs(new_y - tail_y) >= 2:
        tail_y += np.sign(new_y - tail_y)
        if abs(new_x - tail_x) >= 1:
            tail_x += np.sign(new_x - tail_x)
    return tail_x, tail_y


def print_locations(rope, locations, width, height):
    a = np.zeros((width, height), dtype=int)
    for location in locations:
        x, y = location
        a[y, x] = -1
    for i, pos in enumerate(rope):
        x, y = pos
        a[y, x] = len(rope) - i + 1
    print(a[::-1])
    return


def parse_input(moves):
    rope = [(11, 5) for _ in range(10)]
    head_x, head_y = rope[-1]
    tail_x, tail_y = rope[0]
    tail_location_list = {(tail_x, tail_y)}
    for line in moves.splitlines(keepends=False):
        direction, amount_str = line.split(' ')
        amount = int(amount_str)
        for move in range(amount):
            x_step, y_step = direction_step[direction]
            head_x += x_step
            head_y += y_step
            rope[-1] = (head_x, head_y)
            for i in range(len(rope) - 1):
                first_seg = rope[-i - 1]
                second_seg = rope[-i - 2]
                first_x, first_y = first_seg
                second_x, second_y = second_seg
                tail_x, tail_y = calc_tail_pos((first_x, first_y), (second_x, second_y))
                rope[-i - 2] = tail_x, tail_y
            print(tail_x, tail_y)
            tail_location_list.add((tail_x, tail_y))
            # print_locations(rope, tail_location_list, 21 + 1, len('..........................') + 1)
        # print_locations(rope, tail_location_list, 21 + 1, len('..........................') + 1)
    return tail_location_list

tail_location_list = parse_input(test_input)
print(f'{tail_location_list=}')
print(f'{len(tail_location_list)=}')


tail_location_list = parse_input(open('day9-input.txt').read())
# print(f'{tail_location_list=}')
print(f'{len(tail_location_list)=}')
