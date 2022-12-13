# Notes:
# For all points with height "a", see which one has the shortest path to the
# finish.

import numpy as np
from numba import njit

np.set_printoptions(edgeitems=30, linewidth=100000)

test_input = """\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""


def parse_input(s):
    rows = s.count('\n')
    cols = s.index('\n')
    heights = np.zeros((rows, cols), dtype=int)
    row = 0
    col = 0
    for c in s:
        if c == '\n':
            row += 1
            col = 0
            continue
        elif c == 'S':
            height = 0
            start = row, col
        elif c == 'E':
            height = 26
            end = row, col
        else:
            height = ord(c) - ord('a')
        heights[row, col] = height
        col += 1
    visited = np.zeros_like(heights, dtype=int)
    return heights, visited, start, end


def can_move(heights, visited, position, new_position):
    rows, cols = heights.shape
    if new_position[0] < 0 or new_position[0] >= rows:
        return False
    if new_position[1] < 0 or new_position[1] >= cols:
        return False
    if visited[new_position] == 1:
        # Already visited
        return False
    old_height = heights[position]
    new_height = heights[new_position]
    if new_height - old_height > 1:
        return False
    return True


def find_options(heights, visited, position):
    possible_y = [1, -1, 0, 0]
    possible_x = [0, 0, 1, -1]
    options = []
    for i in range(len(possible_y)):
        new_position = position[0] + possible_y[i], position[1] + possible_x[i]
        if can_move(heights, visited, position, new_position):
            options.append(new_position)
    return options


def walk_back(prev, position):
    steps = 0
    while position is not None:
        position = prev[position]
        steps += 1
    return steps - 1


def bfs(heights, visited, start, end):
    queue = []
    queue.append(start)
    queue_index = 0
    position = queue[queue_index]
    visited[position] = 1
    prev = np.empty_like(heights, dtype=object)
    while position != end:
        options = find_options(heights, visited, position)
        for option in options:
            if option not in queue:
                queue.append(option)
                prev[option] = position
        queue_index += 1
        visited[position] = 1
        if queue_index == len(queue):
            return 9999999
        position = queue[queue_index]
        # print(queue_index, queue)
        # print(visited)
        # print(queue_index)
    # print(prev)
    steps = walk_back(prev, end)
    return steps


def possible_starts(heights):
    possible = np.argwhere(heights == 0)
    return possible


heights_, visited_, start_, end_ = parse_input(test_input)
starts = possible_starts(heights_)
steps_ = np.zeros(starts.shape[0], dtype=int)
print(starts)
for i, start_ in enumerate(starts):
    visited_ = np.zeros_like(heights_)
    steps_for_start = bfs(heights_, visited_, tuple(start_), end_)
    steps_[i] = steps_for_start
    print(f'{start_=}, {steps_for_start}')
print(f'{np.min(steps_)=}, {steps_=}')

# heights_, visited_, start_, end_ = parse_input(open('day12-input.txt').read())
# steps = bfs(heights_, visited_, start_, end_)
# print(f'{steps=}')


heights_, visited_, start_, end_ = parse_input(open('day12-input.txt').read())
starts = possible_starts(heights_)
steps_ = np.zeros(starts.shape[0], dtype=int)
print(starts)
for i, start_ in enumerate(starts):
    visited_ = np.zeros_like(heights_)
    steps_for_start = bfs(heights_, visited_, tuple(start_), end_)
    steps_[i] = steps_for_start
    if steps_for_start != 9999999:
        print(f'{start_=}, {steps_for_start}')
print(f'{np.min(steps_)=}, {steps_=}')
