# Notes
# Moving around a map
# There is no turn at the end of the input, so to make parsing easier, pretend
# we start facing up, and the first instruction is to turn right

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


def wrap_around(r, c, m):
    if r < 0:
        r += m.shape[0]
    elif r >= m.shape[0]:
        r -= m.shape[0]
    elif c < 0:
        c += m.shape[1]
    elif c >= m.shape[1]:
        c -= m.shape[1]
    return r, c


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
    keep_trying = True
    while keep_trying:
        r += r_inc
        c += c_inc
        possible_next_position = wrap_around(r, c, m)
        contents = m[possible_next_position]
        if contents == TILE_WALL:
            # Can not move
            next_position = possible_next_position
            break
        elif contents > 0:
            # Can move
            next_position = possible_next_position
            break
        else:
            # The void
            pass
    return next_position


def move_single(m, position, facing):
    done = False
    next_position = next_cell(m, position, facing)
    contents = m[next_position]
    if contents == TILE_WALL:
        done = True
    else:
        position = next_position
    m[position] = facing
    return done, position


def execute_move(m, position, facing, move):
    count, rotation = move
    facing = change_facing(facing, rotation)
    m[position] = facing
    done = False
    while not done and count > 0:
        done, position = move_single(m, position, facing)
        count -= 1
    # print_map(m)
    return position, facing


map_ = parse_map(test_map)
moves_ = parse_moves(test_directions)
position_ = find_start_pos(map_)
facing_ = FACING_UP
for move in moves_:
    position_, facing_ = execute_move(map_, position_, facing_, move)
row, col = position_
# print_map(map_)
# print(row, col, facing_, '=', (row+1) * 1000 + (col+1) * 4 + facing_ - 2)

map_ = parse_map(open('day22-input-1.txt').read())
moves_ = parse_moves(open('day22-input-2.txt').read())
position_ = find_start_pos(map_)
facing_ = FACING_UP
for move_num, move in enumerate(moves_):
    position_, facing_ = execute_move(map_, position_, facing_, move)
row, col = position_
print_map(map_)
print(row, col, facing_, '=', (row+1) * 1000 + (col+1) * 4 + facing_ - 2)
# Too low: 43465, 14222
# Too high: 156 36 5 = 157151
