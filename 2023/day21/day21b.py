from typing import Tuple, Set

import numpy as np
import numba as nb
import matplotlib as mpl
from matplotlib import pyplot as plt

np.set_printoptions(threshold=np.inf, linewidth=100000)

# Middle row is empty... so the elf will be able to get to the edge in
# the same number of steps as half the puzzle width.
# So, for 26501365 steps, we are looking at 26501365//131 = 202300 iterations
# plus 65 left over.
# Getting the size of 4 and 5 iterations using a 2 degree poly fit checks out:
"""
>>> xs=[65,196,327]
>>> ys=[3751,33531,92991]
>>> z=np.polyfit(xs,ys,2)
>>> p=np.poly1d(z)
>>> p(65+131*3)
182131.0000000001
>>> p(65+131*4)
300951.0000000001

"""
# So, this should be the answer for 202300 iterations: p(65+131*202300)

example = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


START = 0
GARDEN = 0
ROCK = 1

lookup = {
    'S': START,
    '.': GARDEN,
    '#': ROCK
}

def parse(lines: str) -> Tuple[np.ndarray, int, int, int]:
    split = lines.splitlines()
    maze = np.empty((len(split), len(split[0])), dtype=int)
    for i, line in enumerate(split):
        for j, c in enumerate(line):
            maze[i,j] = lookup[c]
            if c == 'S':
                y, x = i, j
    # Make it bigger
    scale_factor = 9
    maze_height, maze_width = maze.shape
    scaled_maze = np.empty((maze_height*scale_factor, maze_width*scale_factor), dtype=int)
    for i in range(scale_factor):
        for j in range(scale_factor):
            scaled_maze[i*maze_height:(i+1)*maze_width,j*maze_height:(j+1)*maze_width]=maze
    return scaled_maze, maze_height, int(y + maze_height*(scale_factor-1)/2), int(x+maze_width*(scale_factor-1)/2)

@nb.njit
def valid_positions(maze, y, x):
    possible = [
        (y - 1, x),
        (y + 1, x),
        (y, x + 1),
        (y, x - 1)
    ]
    valid = []
    for y, x in possible:
        if 0 <= y < maze.shape[0] and 0 <= x < maze.shape[1]:
            if maze[y, x] != ROCK:
                valid.append((y, x))
    return valid

@nb.njit
def next_steps(maze: np.ndarray, prev_steps):
    steps = set()
    for prev_step in prev_steps:
        y, x = prev_step
        for position in valid_positions(maze, y, x):
            step = position[0], position[1]
            steps.add(step)
    return steps

def show_maze(maze, steps):
    maze = np.copy(maze)
    for y,x in steps:
        maze[y,x] = 2
    cmap_list = (
        # 0: Garden
        (1, 1, 1, 1),
        # 1: Rock
        (0, 0, 0, 1),
        # 2: Elf
        (1, 0, 0, 1),
    )
    cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmap_list, 3)
    fig, ax = plt.subplots(1, 1)
    ax.imshow(maze, cmap=cmap)
    plt.show()
    return

@nb.njit
def min_y(start_height, orig_height, steps):
    min_y = np.inf
    for step in steps:
        min_y = min(step[0], min_y)
    return min_y

@nb.njit
def min_x(start_height, orig_height, steps):
    min_x = np.inf
    for step in steps:
        min_x = min(step[1], min_1)
    return min_1

def solve(lines, step_count):
    maze, orig_height, y, x = parse(lines)
    steps = {(y, x)}
    for count in range(step_count):
        steps = next_steps(maze, steps)
        lowest_row = min_y(orig_height, y, steps)
        lowest_col = min_y(orig_height, y, steps)
        if lowest_row%orig_height==0:
            print(count+1, len(steps), lowest_row, lowest_col)
            show_maze(maze, steps)
    return

if __name__ == '__main__':
    # solve(example, 500)
    solve(open('input.txt').read(), 600)
