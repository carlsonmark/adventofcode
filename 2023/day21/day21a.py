from typing import Tuple

import numpy as np

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


START = 1
GARDEN = 1
ROCK = 2
FINAL = 3

lookup = {
    'S': START,
    '.': GARDEN,
    '#': ROCK
}

def parse(lines: str) -> Tuple[np.ndarray, int, int]:
    split = lines.splitlines()
    maze = np.empty((len(split), len(split[0])), dtype=int)
    for i, line in enumerate(split):
        for j, c in enumerate(line):
            maze[i,j] = lookup[c]
            if c == 'S':
                y, x = i, j
    return maze, y, x

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


def next_steps(maze, prev_steps, count):
    steps = set()
    for prev_step in prev_steps:
        y, x, _ = prev_step
        for position in valid_positions(maze, y, x):
            step = position[0], position[1], count+1
            steps.add(step)
    return steps

def solve(lines, step_count):
    maze, y, x = parse(lines)
    steps = {(y, x, -1)}
    for count in range(step_count):
        steps = next_steps(maze, steps, count)
    print(len(steps), steps)
    return

if __name__ == '__main__':
    solve(example, 6)
    solve(open('input.txt').read(), 64)
