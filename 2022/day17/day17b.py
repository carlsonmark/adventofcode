# Notes
# Those dang elephants want to know how tall the tower will be after 1000000000000 rocks have been dropped
# That's way too many to fully simulate
# I bet there is some repetition... related to the number of rocks and moves
# Check how high it is after rocks*moves and rocks*moves*2, I bet the latter is double the former
# Then try to leverage modular arithmetic somehow
# See how many times the pattern repeats, and how many rocks are left over?
# Then simulate one full loop plus the leftover and use that to top up the total

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


def height_for_desired(jets, desired_rocks):
    arena_ = np.zeros((len(jets)*len(ROCKS), 7), dtype=int)
    move_count_ = 0
    probable_first_location_ = 0
    num_rocks = len(ROCKS)
    num_jets = len(jets)
    cache = {}

    for rock_number_ in range(desired_rocks):
        move_count_, probable_first_location_ = drop_rock(arena_, jets, rock_number_, move_count_, probable_first_location_)
        row, col = spawn_location(arena_, probable_first_location_)
        row += 5
        height = arena_.shape[0] - row
        rock_rem = rock_number_ % num_rocks
        jet_rem = move_count_ % num_jets
        key = (rock_rem, jet_rem)
        if key in cache:
            prev_rock_num, prev_height = cache[key]
            period = rock_number_ - prev_rock_num
            # Alright, found it, but keep going until the next cycle of the period for an easier calculation
            if rock_number_ % period == desired_rocks % period:
                print(cache)
                print(f'repetition found: {rock_number_} {period=} {key}, {cache[key]}')
                cycle_height = height - prev_height
                remaining = desired_rocks - rock_number_
                cycles_remaining = (remaining // period) + 1
                return prev_height + (cycle_height * cycles_remaining)

        cache[(rock_rem, jet_rem)] = (rock_number_, height)
    return height


def get_top(arena, probable_spawn_location):
    row, col = spawn_location(arena, probable_spawn_location)
    row += 4
    if row >= arena.shape[0]:
        return np.ones(7)
    return arena[row]


def get_top(arena, probable_spawn_location):
    row, col = spawn_location(arena, probable_spawn_location)
    row += 4
    if row >= arena.shape[0]:
        return np.ones(7)
    return arena[row]


jets_ = test_input.strip('\n')
height = height_for_desired(jets_, 2022)
print(height)

height = height_for_desired(jets_, 1000000000000)
print(height)

jets_ = open('day17-input.txt').read().strip('\n')
height = height_for_desired(jets_, 2022)
print(height)

height = height_for_desired(jets_, 1000000000000)
print(height)  # 1523615160363 too high... I just tried again with -1, and it worked... not sure why I am close but not quite there!

