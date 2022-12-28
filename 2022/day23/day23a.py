# Notes
# Magma flow
# Plant seeds in ash, elves are "#" and empty ground is "."
# More empty ground outside the scanned area in every direction
# Elves want to spread out so there are no elves in adjacent to them
# First half of round is to consider the movement:
# - If no elf in any of the 8 positions, no move
# - If no elf in N, NE, or NW, move N
# - If no elf in S, SE, or SW, move S
# - If no elf in W, NW, or SW, move W
# - If no elf in E, NE, or SE, move E
# Second half of the round:
# - Execute move if they are the only elf to move to that position
# - Otherwise, they do not move
# After 10 rounds, find the smallest rectangle that contains the elves, then
# count the number of empty ground tiles

import numpy as np

test_input = """\
..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............
"""


def create_map(s: str):
    # Load the map, but make it have 10 extra pairs of rows and columns to
    # allow for maximum movement
    lines = s.splitlines(keepends=False)
    cols = len(lines)
    rows = len(lines[0])
    shape = rows + 20, cols + 20
    m = np.zeros(shape, dtype=int)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '#':
                # Elf
                m[row + 10, col + 10] = 1
    return m


def propose_move(m, row, col, round_number):
    northy_count = sum(m[row-1, col-1:col+2])
    southy_count = sum(m[row+1, col-1:col+2])
    westy_count = sum(m[row-1:row+2, col-1])
    easty_count = sum(m[row-1:row+2, col+1])
    move = (row, col)
    if sum((northy_count, southy_count, westy_count, easty_count)) == 0:
        # No need to move
        move = (row, col)
    elif round_number % 4 == 0:
        if northy_count == 0:
            move = (row - 1, col)
        elif southy_count == 0:
            move = (row + 1, col)
        elif westy_count == 0:
            move = (row, col - 1)
        elif easty_count == 0:
            move = (row, col + 1)
    elif round_number % 4 == 1:
        if southy_count == 0:
            move = (row + 1, col)
        elif westy_count == 0:
            move = (row, col - 1)
        elif easty_count == 0:
            move = (row, col + 1)
        elif northy_count == 0:
            move = (row - 1, col)
    elif round_number % 4 == 2:
        if westy_count == 0:
            move = (row, col - 1)
        elif easty_count == 0:
            move = (row, col + 1)
        elif northy_count == 0:
            move = (row - 1, col)
        elif southy_count == 0:
            move = (row + 1, col)
    elif round_number % 4 == 3:
        if easty_count == 0:
            move = (row, col + 1)
        elif northy_count == 0:
            move = (row - 1, col)
        elif southy_count == 0:
            move = (row + 1, col)
        elif westy_count == 0:
            move = (row, col - 1)
    return move


def propose_moves(m, round_number):
    moves = {}  # from: to
    for row, col in np.ndindex(m.shape):
        if m[row, col] == 1:
            move = propose_move(m, row, col, round_number)
            moves[(row, col)] = move
    return moves


def filter_moves(moves):
    # Check for duplicate destinations
    # Remove all offenders
    # Also, remove any that would have moved into the source of any of the
    # offenders.
    # Repeat until no offences were found
    found_invalid_move = True
    all_destinations = []
    while found_invalid_move:
        found_invalid_move = False
        all_destinations = []
        invalid_from_coords = []
        all_to_coords = list(moves.values())
        for from_coord, to_coord in moves.items():
            if all_to_coords.count(to_coord) > 1:
                # Duplicate!
                found_invalid_move = True
                invalid_from_coords.append(from_coord)
            all_destinations.append(to_coord)
        # Change duplicates so they don't move
        for coord in invalid_from_coords:
            moves[coord] = coord
    return all_destinations


def execute_moves(m, all_destinations):
    m2 = np.zeros_like(m)
    # Fill in the locations for the valid destinations
    for destination in all_destinations:
        m2[destination] = 1
    return m2


def print_map(m):
    rows, cols = m.shape
    for row in range(rows):
        for col in range(cols):
            if m[row, col] == 1:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()
    return


def score_map(m):
    rows, cols = m.shape
    for start_row in range(rows):
        if sum(m[start_row, :]) > 0:
            break
    for end_row in reversed(range(rows)):
        if sum(m[end_row, :]) > 0:
            break
    for start_col in range(cols):
        if sum(m[:, start_col]) > 0:
            break
    for end_col in reversed(range(cols)):
        if sum(m[:, end_col]) > 0:
            break
    sub_mat = m[start_row:end_row+1, start_col:end_col+1]
    return np.sum(np.where(sub_mat == 0, 1, 0))


m_ = create_map(test_input)
print_map(m_)
for round_number in range(10):
    moves_ = propose_moves(m_, round_number)
    destinations_ = filter_moves(moves_)
    m_ = execute_moves(m_, destinations_)
    print(f'After round {round_number + 1}')
    print_map(m_)

print(f'{score_map(m_)=}')

m_ = create_map(open('day23-input.txt').read())
for round_number in range(10):
    moves_ = propose_moves(m_, round_number)
    destinations_ = filter_moves(moves_)
    m_ = execute_moves(m_, destinations_)
    print(f'After round {round_number + 1}')

print_map(m_)
print(f'{score_map(m_)=}')
