# Notes
# Sand simulation, same rules from a
# Bottom is floor, and is at y=2+max_y
# How much sand before hitting the top of the cave?

import numpy as np

test_input = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""


def draw_line(cave, start, end):
    inc_x = 0
    if start[0] > end[0]:
        inc_x = -1
    elif start[0] < end[0]:
        inc_x = 1
    inc_y = 0
    if start[1] > end[1]:
        inc_y = -1
    elif start[1] < end[1]:
        inc_y = 1
    pos = start
    while pos != end:
        cave[pos] = 1
        pos = pos[0] + inc_x, pos[1] + inc_y
    cave[end] = 1
    return


def parse_input(s):
    coords = []
    all_xs = []
    all_ys = []
    for line in s.splitlines(keepends=False):
        line_coords_strs = line.split(' -> ')
        line_coords = []
        for coord_str in line_coords_strs:
            print(coord_str)
            x_s, y_s = coord_str.split(',')
            x = int(x_s)
            all_xs.append(x)
            y = int(y_s)
            all_ys.append(y)
            line_coords.append((x,y))
        coords.append(line_coords)
    max_x = max(all_xs)
    max_y = max(all_ys)
    cave_bottom = max_y + 3
    cave_left = min(all_xs) - 1
    cave_right = max_x + 1
    cave = np.zeros((max_x * 2, max_y + 3), dtype=int)
    for line_coords in coords:
        start = line_coords[0]
        line_coords = line_coords[1:]
        while line_coords:
            end = line_coords[0]
            draw_line(cave, start, end)
            line_coords = line_coords[1:]
            start = end
    cave.T[-1] = 1
    return cave_bottom, cave_left, cave_right, cave


def print_cave(cave, left, right, bottom):
    for row in cave.T[:bottom]:
        for c in row[left:right+1]:
            if c == 0:
                print('.', end='')
            elif c == 1:
                print('#', end='')
            elif c == 2:
                print('o', end='')
        print()
    print()
    return


def drop_sand(cave, cave_bottom):
    origin = (500, 0)
    sand_pos = origin
    first = True
    while first or sand_pos != origin:
        first = False
        down_pos = sand_pos[0], sand_pos[1] + 1
        bot_left_pos = down_pos[0] - 1, down_pos[1]
        bot_right_pos = down_pos[0] + 1, down_pos[1]
        if cave[down_pos] == 0:
            sand_pos = down_pos
        elif cave[bot_left_pos] == 0:
            sand_pos = bot_left_pos
        elif cave[bot_right_pos] == 0:
            sand_pos = bot_right_pos
        else:
            break
    cave[sand_pos] = 2
    return sand_pos == origin


cave_bottom_, cave_left_, cave_right_, cave_ = parse_input(test_input)
print_cave(cave_, cave_left_, cave_right_, cave_bottom_)
sand_count = 0
while not drop_sand(cave_, cave_bottom_):
    sand_count += 1
    print_cave(cave_, cave_left_, cave_right_, cave_bottom_)
print(f'{sand_count+1=}')

cave_bottom_, cave_left_, cave_right_, cave_ = parse_input(open('day14-input.txt').read())
print_cave(cave_, cave_left_, cave_right_, cave_bottom_)
sand_count = 0
while not drop_sand(cave_, cave_bottom_):
    sand_count += 1
    if sand_count % 50 == 0:
        print_cave(cave_, cave_left_, cave_right_, cave_bottom_)
print(f'{sand_count+1=}')
