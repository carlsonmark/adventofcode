# Notes
# Keep going until they stop moving
# The solution is the count of moves

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
    # Load the map, but make it have 3x the rows and columns
    # allow for maximum movement
    lines = s.splitlines(keepends=False)
    cols = len(lines)
    rows = len(lines[0])
    shape = rows * 3, cols * 3
    m = np.zeros(shape, dtype=np.int8)
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '#':
                # Elf
                m[row + rows, col + cols] = 1
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
still_moving = True
move_count = 0
while still_moving:
    moves_ = propose_moves(m_, move_count)
    destinations_ = filter_moves(moves_)
    m_moved = execute_moves(m_, destinations_)
    if (m_moved == m_).all():
        still_moving = False
    m_ = m_moved
    print(f'After round {move_count + 1}')
    print_map(m_)
    move_count += 1

print(f'{move_count=}')

m_ = create_map(open('day23-input.txt').read())
print_map(m_)
still_moving = True
move_count = 0
while still_moving:
    moves_ = propose_moves(m_, move_count)
    destinations_ = filter_moves(moves_)
    m_moved = execute_moves(m_, destinations_)
    if (m_moved == m_).all():
        still_moving = False
    m_ = m_moved
    print(f'After round {move_count + 1}')
    # print_map(m_)
    move_count += 1

print_map(m_)
print(f'{move_count=}')
