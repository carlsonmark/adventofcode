# Notes
# Moving around a map
# There is no turn at the end of the input, so to make parsing easier, pretend
# we start facing up, and the first instruction is to turn right
# This time it is on a cube... Hopefully I only need to change a few things,
# even if those changes will be tricky!
# The wrapping code will need to:
# - Take in the current facing
# - Return the new facing
# Only use the new facing if the position was also used

import re
from typing import Tuple, List

import numpy as np

test_map = """\
        ...#    
        .#..    
        #...    
        ....    
...#.......#    
........#...    
..#....#....    
..........#.    
        ...#....
        .....#..
        .#......
        ......#.
"""

test_directions = "10R5L5R10L4R5L5"


TILE_EMPTY = -1
TILE_FLOOR = 1
TILE_WALL = 0
FACING_RIGHT = 2
FACING_DOWN = 3
FACING_LEFT = 4
FACING_UP = 5


def parse_map(s: str):
    lines = s.splitlines(keepends=False)
    shape = len(lines), len(lines[0])
    m = np.ones(shape, dtype=int) * -1
    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == ' ':
                m[row][col] = TILE_EMPTY
            elif c == '.':
                m[row][col] = TILE_FLOOR
            elif c == '#':
                m[row][col] = TILE_WALL
    return m


def print_map(m):
    rows, cols = m.shape
    lookup_table = {
        TILE_EMPTY: ' ',
        TILE_FLOOR: '.',
        TILE_WALL: '#',
        FACING_RIGHT: '>',
        FACING_DOWN: 'V',
        FACING_LEFT: '<',
        FACING_UP: '^',
    }
    for row in range(rows):
        for col in range(cols):
            val = m[row, col]
            c = lookup_table[val]
            print(c, end='')
        print()
    print()
    return


def parse_moves(s: str) -> List[Tuple[int, str]]:
    moves = []
    found = re.findall(r'.\d+', 'R' + s)
    for f in found:
        rotation = f[0]
        n = int(f[1:])
        moves.append((n, rotation))
    return moves


def find_start_pos(m):
    for col, c in enumerate(m[0]):
        if c == TILE_FLOOR:
            return 0, col
    return


def change_facing(initial_facing, rotation):
    if initial_facing == FACING_RIGHT:
        new_facing = FACING_UP
        if rotation == 'R':
            new_facing = FACING_DOWN
    elif initial_facing == FACING_DOWN:
        new_facing = FACING_RIGHT
        if rotation == 'R':
            new_facing = FACING_LEFT
    elif initial_facing == FACING_LEFT:
        new_facing = FACING_DOWN
        if rotation == 'R':
            new_facing = FACING_UP
    elif initial_facing == FACING_UP:
        new_facing = FACING_LEFT
        if rotation == 'R':
            new_facing = FACING_RIGHT
    return new_facing


def wrap_around(r, c, m, facing):
    if facing == FACING_LEFT:
        if c == -1:
            if 100 <= r < 150:
                # Flip
                facing = FACING_RIGHT
                c = 50
                r = 149 - r
            else:
                facing = FACING_DOWN
                c = r - 100
                r = 0
        elif c == 49:
            if 0 <= r < 50:
                # Flip
                facing = FACING_RIGHT
                r = 149 - r
                c = 0
            if 50 <= r < 100:
                facing = FACING_DOWN
                c = r - 50
                r = 100
    elif facing == FACING_RIGHT:
        if c == 50:
            if r >= 150:
                facing = FACING_UP
                c = r - 100
                r = 149
        elif c == 100:
            if 100 <= r < 150:
                # Flip
                facing = FACING_LEFT
                r = 149 - r
                c = 149
            elif 50 <= r < 100:
                facing = FACING_UP
                c = r + 50
                r = 49
        elif c == 150:
            # Flip
            facing = FACING_LEFT
            r = 149 - r
            c = 99
    elif facing == FACING_UP:
        if r == -1:
            if 50 <= c < 100:
                facing = FACING_RIGHT
                r = c + 100
                c = 0
            else:
                # NO-FLIP
                facing = FACING_UP
                c = c - 100
                r = 199
        elif r == 99:
            if 0 <= c < 50:
                facing = FACING_RIGHT
                r = c + 50
                c = 50
    else:
        if r == 50:
            if 100 <= c < 150:
                facing = FACING_LEFT
                r = c - 50
                c = 99
        elif r == 150:
            if 50 <= c < 100:
                facing = FACING_LEFT
                r = c + 100
                c = 49
        elif r == 200:
            # NO-FLIP
            facing = FACING_DOWN
            c = c + 100
            r = 0

    return r, c, facing


def next_cell(m, position, facing):
    r, c = position
    r_inc = 0
    c_inc = 0
    if facing == FACING_RIGHT:
        c_inc = 1
    elif facing == FACING_DOWN:
        r_inc = 1
    elif facing == FACING_LEFT:
        c_inc = -1
    else:
        r_inc = -1
    next_facing = facing
    r += r_inc
    c += c_inc
    new_r, new_c, possible_next_facing = wrap_around(r, c, m, next_facing)
    possible_next_position = new_r, new_c
    contents = m[possible_next_position]
    if contents == TILE_WALL:
        # Can not move
        next_position = position
        next_facing = facing
    elif contents > 0:
        # Can move
        next_position = possible_next_position
        next_facing = possible_next_facing
    else:
        # The void
        raise Exception('The VOID!')
    return next_position, next_facing


def move_single(m, position, facing):
    done = False
    next_position, next_facing = next_cell(m, position, facing)
    contents = m[next_position]
    if contents == TILE_WALL:
        done = True
    else:
        position = next_position
        facing = next_facing
    m[position] = facing
    return done, position, facing


def execute_move(m, position, facing, move):
    count, rotation = move
    facing = change_facing(facing, rotation)
    m[position] = facing
    done = False
    while not done and count > 0:
        done, position, facing = move_single(m, position, facing)
        count -= 1
    # print_map(m)
    return position, facing


# map_ = parse_map(test_map)
# moves_ = parse_moves(test_directions)
# position_ = find_start_pos(map_)
# facing_ = FACING_UP
# for move in moves_:
#     position_, facing_ = execute_move(map_, position_, facing_, move)
# row, col = position_
# print_map(map_)
# print(row, col, facing_, '=', (row+1) * 1000 + (col+1) * 4 + facing_ - 2)

map_ = parse_map(open('day22-input-1.txt').read())
map_ = np.where(map_ < 0, map_, 1)
# moves_ = parse_moves(open('day22-input-2.txt').read())
moves_ = [(195, 'R'), (195, 'R'), (195, 'R'), (195, 'R')]
moves_ = [(200, 'L'), (200, 'L'), (200, 'L'), (200, 'L')]
position_ = 49, 99
facing_ = FACING_DOWN
for move_num, move in enumerate(moves_[:20]):
    position_, facing_ = execute_move(map_, position_, facing_, move)
    print_map(map_)
row, col = position_
print_map(map_)
print(row, col, facing_, '=', (row+1) * 1000 + (col+1) * 4 + facing_ - 2)

map_ = parse_map(open('day22-input-1.txt').read())
moves_ = parse_moves(open('day22-input-2.txt').read())
position_ = find_start_pos(map_)
facing_ = FACING_UP
for move_num, move in enumerate(moves_):
    position_, facing_ = execute_move(map_, position_, facing_, move)
row, col = position_
print_map(map_)
print(row, col, facing_, '=', (row+1) * 1000 + (col+1) * 4 + facing_ - 2)

# Too low: 34 89 3 = 35361
