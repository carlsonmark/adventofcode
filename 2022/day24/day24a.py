# Notes
# Blizzard!
# Avoid the blizzards
# Input is a map of the valley and the blizzards
# # - Walls
# . - Ground
# Arrow - The direction of the blizzard
# When blizzards reach the wall of the valley, a new blizzard forms on the
# opposite side, but moving in the same direction.
# Blizzards pass through each other and can occupy the same spot
# Each turn, you can move up, down, left, or right, or wait, but you can not
# share a position with a blizzard.
# DFS I think? Usually this is quite slow, but the number of options should be
# fairly limited?
# Optimizations:
# - Cache best moves
# - List of blizzards is too slow to copy, use a numpy array for blizzards, but
#   use individual bits to represent the blizzard direction...
#   More work for the moving code, but waaaay faster copy time
import numpy as np
import sys
RECURSION_LIMIT = 1000
sys.setrecursionlimit(RECURSION_LIMIT + 10)

test_input = """\
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""

DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 4
DIR_LEFT = 8
DIR_NONE = 16

DIR_CHARS = {
    DIR_UP: '^',
    DIR_RIGHT: '>',
    DIR_DOWN: 'v',
    DIR_LEFT: '<',
    DIR_NONE: 'N'
}


def parse_input(s: str):
    lines = s.splitlines(keepends=False)[1:-1]
    # Trim off the outer square
    rows = len(lines)
    cols = len(lines[0]) - 2
    m = np.zeros((rows, cols), dtype=np.uint8)
    elf_pos = -1, 0
    for row, line in enumerate(lines):
        for col, char in enumerate(line[1: -1]):
            if char == '^':
                m[row, col] = DIR_UP
            elif char == '>':
                m[row, col] = DIR_RIGHT
            elif char == 'v':
                m[row, col] = DIR_DOWN
            elif char == '<':
                m[row, col] = DIR_LEFT
    return m, elf_pos


def print_blizzards(m, elf_pos):
    rows, cols = m.shape
    for row in range(rows):
        for col in range(cols):
            num_blizzards = m[row, col].bit_count()
            if (row, col) == elf_pos:
                print('E', end='')
            elif num_blizzards == 0:
                print('.', end='')
            elif num_blizzards > 1:
                print(str(num_blizzards), end='')
            elif num_blizzards == 1:
                blizzard_dir = m[row, col]
                print(DIR_CHARS[blizzard_dir], end='')
        print()
    print()
    return


def moves(m, elf_pos):
    moves_ = set()
    rows, cols = m.shape
    row, col = elf_pos
    if elf_pos == (-1, 0):
        # Special case: First move
        if m[0, 0] == 0:
            moves_ = {DIR_DOWN, DIR_NONE}
        else:
            moves_ = {DIR_NONE}
    elif elf_pos == (rows - 1, cols - 1):
        # Special case: End
        moves_ = {DIR_DOWN}
    else:
        # Check for blizzards
        if col < (cols - 1) and m[row, col + 1] == 0:
            moves_.add(DIR_RIGHT)
        if row < (rows - 1) and m[row + 1, col] == 0:
            moves_.add(DIR_DOWN)
        if col > 0 and m[row, col - 1] == 0:
            moves_.add(DIR_LEFT)
        if row > 0 and m[row - 1, col] == 0:
            moves_.add(DIR_UP)
        if m[elf_pos] == 0:
            moves_.add(DIR_NONE)
    return moves_


def move_blizzards(m):
    bliz_up = m & DIR_UP
    bliz_right = m & DIR_RIGHT
    bliz_down = m & DIR_DOWN
    bliz_left = m & DIR_LEFT
    bliz_up = np.roll(bliz_up, -1, 0)
    bliz_down = np.roll(bliz_down, 1, 0)
    bliz_right = np.roll(bliz_right, 1, 1)
    bliz_left = np.roll(bliz_left, -1, 1)
    return bliz_up | bliz_down | bliz_right | bliz_left


def move_elf(elf_pos, move):
    row, col = elf_pos
    if move == DIR_UP:
        row -= 1
    elif move == DIR_RIGHT:
        col += 1
    elif move == DIR_DOWN:
        row += 1
    elif move == DIR_LEFT:
        col -= 1
    return row, col


class BlizzardCasualty(Exception):
    pass


# (move_count, elf_pos): best_move_count
cache = {}


def find_optimal_path(m, elf_pos, move_count, best_move_count):
    move_count += 1
    if move_count >= best_move_count:
        # Might as well have been lost to a blizzard
        raise BlizzardCasualty()
    rows, cols = m.shape
    row, col = elf_pos
    # Hopefully the branches will complete before this!
    too_long = (rows + cols) * 3 - (rows - row) - (cols - col)
    if move_count > too_long:
        # Might as well have been lost to a blizzard
        raise BlizzardCasualty()
    m = move_blizzards(m)
    moves_ = moves(m, elf_pos)
    if len(moves_) == 0:
        # Uh oh, another one lost to the blizzards!
        raise BlizzardCasualty()
    orig_elf_pos = elf_pos
    move_counts = [best_move_count]
    for move in moves_:
        elf_pos = move_elf(orig_elf_pos, move)
        # print(f'{move_count=}, {elf_pos=} {DIR_CHARS[move]=} {[DIR_CHARS[move] for move in moves_]}')
        # print_blizzards(m, elf_pos)
        if elf_pos == (rows-1, cols-1):
            # Done!
            print('Found new end:', move_count)
            best_move_count = move_count + 1
            return best_move_count
        try:
            cached = cache.get((move_count, elf_pos))
            if cached is not None:
                # print(f'Cache hit: {move_count=}, {elf_pos=}, {cached}')
                move_counts.append(cached)
            else:
                this_best_move_count = find_optimal_path(m.copy(), elf_pos, move_count, best_move_count)
                move_counts.append(this_best_move_count)
            # best_move_count = min(this_best_move_count, best_move_count)
        except BlizzardCasualty:
            pass
    best_move_count = min(move_counts)
    cache[(move_count, elf_pos)] = best_move_count
    return best_move_count


# Part A:

# m_, elf_pos_ = parse_input(test_input)
# rows, cols = m_.shape
# best_move_count_ = find_optimal_path(m_, elf_pos_, move_count=0, best_move_count=999999)
# print('move_count', best_move_count_)

# m_, elf_pos_ = parse_input(open('day24-input.txt').read())
# rows, cols = m_.shape
# best_move_count_ = find_optimal_path(m_, elf_pos_, move_count=0, best_move_count=999999)
# print('move_count', best_move_count_)

# Part B return trip:

# m_, elf_pos_ = parse_input(test_input)
# for i in range(18 + 23):
#     m_ = move_blizzards(m_)
# best_move_count_ = find_optimal_path(m_, elf_pos_, move_count=0, best_move_count=999999)
# print('move_count', best_move_count_)

m_, elf_pos_ = parse_input(open('day24-input.txt').read())
for i in range(305 + 284):
    m_ = move_blizzards(m_)
best_move_count_ = find_optimal_path(m_, elf_pos_, move_count=0, best_move_count=999999)
print('move_count', best_move_count_)
