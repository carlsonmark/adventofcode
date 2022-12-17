# Notes
# Hahaha, tetris simulator?
# Rocks falling from ceiling
# Rock shapes cycle between -, +, _|, |, #
# Moves are the inputs, < is move left one, > is move right one
# If inputs run out, loop them I guess?
# Chamber is 7 units wide
# Rocks start dropping with 2 empty units on the left
# Rocks start dropping from a height where there is 3 units between the rock and the top of the pile
# Moves are always left/right, then down
# Obviously, collision detection is needed
# If something prevents it from falling, the next rock starts falling
# How tall is the tower after 2022 rocks have stopped (before 2023 has started falling)

import numpy as np

test_input = """\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
"""


def print_arena(arena):
    start_row = spawn_location(arena)[0]
    for row in arena[start_row:]:
        for col in row:
            if col == 0:
                print('.', end='')
            elif col == 1:
                print('#', end='')
            else:
                print('@', end='')
        print()
    print()
    return


ROCKS = ['_', '+', 'L', '|', '#']
NUM_ROCKS = len(ROCKS)
ROCK_CELLS = {
    '_': np.array([[0, 0], [0, 1], [0, 2], [0, 3]]),
    '+': np.array([[-2, 1], [-1, 0], [-1, 1], [-1, 2], [0, 1]]),
    'L': np.array([[-2, 2], [-1, 2], [0, 0], [0, 1], [0, 2]]),
    '|': np.array([[-3, 0], [-2, 0], [-1, 0], [0, 0]]),
    '#': np.array([[-1, 0], [-1, 1], [0, 0], [0, 1]])
}


def which_rock(rock_number):
    return ROCKS[rock_number % NUM_ROCKS]


def which_move(jets, move_count):
    return jets[move_count % len(jets)]


def spawn_location(arena, probable_first_row=0):
    # Maybe there is a faster way to do this
    row_number = arena.shape[0]
    for row_number, row in enumerate(arena[probable_first_row:]):
        if sum(row) > 0:
            row_number -= 1
            break
    return row_number + probable_first_row - 4, 2


def compute_rock_cells(location, rock):
    cells = ROCK_CELLS[rock] + location
    return cells


def fill_rock_shape(arena, rock, location, fill_value):
    rock_cells = compute_rock_cells(location, rock)
    for row, col in rock_cells:
        arena[row, col] = fill_value
    return


def print_arena_with_rock(arena, rock, location):
    fill_rock_shape(arena, rock, location, fill_value=2)
    print_arena(arena)
    fill_rock_shape(arena, rock, location, fill_value=0)
    return


def can_rock_go_to_location(arena, location, rock):
    rock_cells = compute_rock_cells(location, rock)
    for row, col in rock_cells:
        if col < 0 or col >= 7:
            return False
        if row >= arena.shape[0]:
            return False
        if arena[row, col]:
            return False
    return True


def drop_rock(arena, jets, rock_number, move_count, probable_first_location_):
    rock = which_rock(rock_number)
    original_spawn_location = spawn_location(arena, probable_first_location_)
    location = original_spawn_location
    # fill_rock_shape(arena, rock, location, 2)
    # Drop_rock 1 row if possible
    at_rest = False
    while not at_rest:
        possible_location = location[0] + 1, location[1]
        if can_rock_go_to_location(arena, possible_location, rock):
            # It was able to drop, can it move?
            location = possible_location
            # print_arena_with_rock(arena, rock, location)
            move = which_move(jets, move_count)
            if move == '<':
                shift = -1
            else:
                shift = 1
            possible_location = location[0], location[1] + shift
            if can_rock_go_to_location(arena, possible_location, rock):
                location = possible_location
                # print_arena_with_rock(arena, rock, location)
            move_count += 1
        else:
            # Can not drop, it is at rest
            at_rest = True
            fill_rock_shape(arena, rock, location, 1)
    return move_count, original_spawn_location[0] - 10


jets_ = test_input.strip('\n')
arena_ = np.zeros((2022*2, 7), dtype=int)
move_count_ = 0
probable_first_location_ = 0
# drop_rock(arena_, jets_, 0, 0)  # deleteme
# print_arena(arena_)

for rock_number_ in range(2022):
    move_count_, probable_first_location_ = drop_rock(arena_, jets_, rock_number_, move_count_, probable_first_location_)
# print_arena(arena_)

row, col = spawn_location(arena_)
row += 5
height = arena_.shape[0] - row
print(f'Height: {height}')

jets_ = open('day17-input.txt').read().strip('\n')
arena_ = np.zeros((2022*4, 7), dtype=int)
move_count_ = 0
probable_first_location_ = 0
# drop_rock(arena_, jets_, 0, 0)  # deleteme
# print_arena(arena_)

for rock_number_ in range(2022):
    move_count_, probable_first_location_ = drop_rock(arena_, jets_, rock_number_, move_count_, probable_first_location_)
# print_arena(arena_)

row, col = spawn_location(arena_)
row += 5
height = arena_.shape[0] - row
print(f'Height: {height}')
