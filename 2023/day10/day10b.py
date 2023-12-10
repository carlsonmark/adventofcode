# Find the number of tiles enclosed by the loop

from enum import IntEnum
from typing import Tuple, List, Optional

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

# Enclosed: 4
example1 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

# Enclosed: 8
example2 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

# Enclosed: 10
example3 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

EMPTY = 0
PIPE = 1
FILLED = 2

class Pipe(IntEnum):
    Ground = 0 # '.'
    Vertical = 1 # '|'
    Horizontal = 2 # '-'
    BendNE = 3 # 'L'
    BendNW = 4 # 'J'
    BendSW = 5 # '7'
    BendSE = 6 # 'F'
    Start = 7 # 'S'

    @classmethod
    def from_char(self, c: str):
        if c == '.':
            return Pipe.Ground
        if c == '|':
            return Pipe.Vertical
        if c == '-':
            return Pipe.Horizontal
        if c == 'L':
            return Pipe.BendNE
        if c == 'J':
            return Pipe.BendNW
        if c == '7':
            return Pipe.BendSW
        if c == 'F':
            return Pipe.BendSE
        if c == 'S':
            return Pipe.Start

    def to_3x3(self) -> np.ndarray:
        arr = np.zeros((3,3), dtype=int)
        # Center is filled for all pipes
        if self != Pipe.Ground:
            arr[1, 1] = 1
        if self in (Pipe.Vertical, Pipe.BendSE, Pipe.BendSW):
            arr[2, 1] = 1  # Bottom
        if self in (Pipe.Vertical, Pipe.BendNE, Pipe.BendNW):
            arr[0, 1] = 1  # Top
        if self in (Pipe.Horizontal, Pipe.BendNW, Pipe.BendSW):
            arr[1, 0] = 1  # Left
        if self in (Pipe.Horizontal, Pipe.BendNE, Pipe.BendSE):
            arr[1, 2] = 1  # Right
        return arr

def calc_start_pipe_shape(pipes: np.ndarray) -> Tuple[Tuple[int, int], Pipe]:
    start_pos = tuple(np.argwhere(pipes == Pipe.Start)[0])
    y, x = start_pos
    start_pipe_shape = Pipe.Start
    try:
        up = pipes[y - 1, x] in (Pipe.Vertical, Pipe.BendSW, Pipe.BendSE)
    except IndexError: up = False
    try:
        down = pipes[y + 1, x] in (Pipe.Vertical, Pipe.BendNW, Pipe.BendNE)
    except IndexError: down = False
    try:
        left = pipes[y, x - 1] in (Pipe.Horizontal, Pipe.BendNE, Pipe.BendSE)
    except IndexError: left = False
    try:
        right = pipes[y, x + 1] in (Pipe.Horizontal, Pipe.BendNW, Pipe.BendSW)
    except IndexError: right = False
    if up and down: start_pipe_shape = Pipe.Vertical
    if left and right: start_pipe_shape = Pipe.Horizontal
    if up and right: start_pipe_shape = Pipe.BendNE
    if up and left: start_pipe_shape = Pipe.BendNW
    if left and down: start_pipe_shape = Pipe.BendSW
    if right and down: start_pipe_shape = Pipe.BendSE
    return start_pos, start_pipe_shape

def pipes_to_fillable(pipes: np.ndarray) -> np.ndarray:
    arr = np.zeros(np.array(pipes.shape) * 3, dtype=int)
    it = np.nditer(pipes, flags=['multi_index'])
    for pipe_int in it:
        pipe_y, pipe_x = it.multi_index
        pixel_x = pipe_x * 3
        pixel_y = pipe_y * 3
        pipe_3x3 = Pipe(pipe_int).to_3x3()
        arr[pixel_y:pixel_y+3, pixel_x:pixel_x+3] = pipe_3x3
    return arr

def find_empty(pos: Tuple[int, int], fillable: np.ndarray) -> List[Tuple[int, int]]:
    y, x = pos
    if y == 0 or x == 0 or y == fillable.shape[0] or x == fillable.shape[1]:
        raise IndexError
    possibilities = [
        (y - 1, x - 1), (y - 1, x), (y - 1, x + 1),
        (y,     x - 1),             (y,     x + 1),
        (y + 1, x - 1), (y + 1, x), (y + 1, x + 1),
    ]
    empty = []
    for possible in possibilities:
        if fillable[possible] == 0:
            empty.append(possible)
    return empty

def fill(start_pos: Tuple[int, int], fillable: np.ndarray) -> Tuple[bool, np.ndarray]:
    fillable = fillable.copy()
    success = True
    fillable[start_pos] = FILLED
    try:
        options = set(find_empty(start_pos, fillable))
        while options:
            # Fill first
            for option in options:
                fillable[option] = FILLED
            # Find new options for each filled position
            next_options = set()
            for option in options:
                for pos in find_empty(option, fillable):
                    next_options.add(pos)
            options = next_options
    except IndexError:
        success = False
    return success, fillable

def next_pos(current_pos: Tuple[int, int], prev_pos: Tuple[int, int], pipes: np.ndarray) -> Optional[Tuple[int, int]]:
    options = []
    y, x = current_pos
    current_pipe = pipes[current_pos]
    directions = {}
    if current_pipe in (Pipe.Start, Pipe.Vertical, Pipe.BendNE, Pipe.BendNW):
        directions[(y - 1, x)] = (Pipe.Vertical, Pipe.BendSE, Pipe.BendSW)  # Up
    if current_pipe in (Pipe.Start, Pipe.Vertical, Pipe.BendSW, Pipe.BendSE):
        directions[(y + 1, x)] = (Pipe.Vertical, Pipe.BendNE, Pipe.BendNW)  # Down
    if current_pipe in (Pipe.Start, Pipe.Horizontal, Pipe.BendNW, Pipe.BendSW):
        directions[(y, x - 1)] = (Pipe.Horizontal, Pipe.BendNE, Pipe.BendSE)  # Left
    if current_pipe in (Pipe.Start, Pipe.Horizontal, Pipe.BendNE, Pipe.BendSE):
        directions[(y, x + 1)] = (Pipe.Horizontal, Pipe.BendNW, Pipe.BendSW)  # Right
    for direction, ok_list in directions.items():
        try:
            pipe = pipes[direction]
            if pipe in ok_list:
                options.append(direction)
        except IndexError:
            pass

    if tuple(prev_pos) in options:
        options.remove(prev_pos)
    if not options:
        return
    return options[0]

def clean(pipes: np.ndarray) -> np.ndarray:
    cleaned = pipes.copy()
    start_pos = tuple(np.argwhere(pipes == Pipe.Start)[0])
    visited = np.zeros_like(pipes)
    visited[start_pos] = 1
    current_pos = next_pos(start_pos, start_pos, pipes)
    prev_pos = start_pos
    while current_pos is not None:
        visited[current_pos] = 1
        next_step_pos = next_pos(current_pos, prev_pos, pipes)
        prev_pos = current_pos
        current_pos = next_step_pos
    it = np.nditer(cleaned, flags=['multi_index'])
    for _ in it:
        if not visited[it.multi_index]:
            cleaned[it.multi_index] = Pipe.Ground
    return cleaned

def parse(lines: str):
    split = lines.splitlines()
    pipes = np.zeros((len(split), len(split[0])), dtype=int)
    for line_no, line in enumerate(lines.splitlines()):
        pipes[line_no] = [Pipe.from_char(c) for c in line]
    return pipes

def show_pipes(pipes):
    cmap_list = (
        # 0: No pipe or fill
        (1, 1, 1, 1),
        # 1: Pipe
        (0, 0, 0, 1),
        # 2: Fill
        (1, 0, 0, 1)
    )
    cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmap_list, 3)
    fig, ax = plt.subplots(1, 1)
    ax.imshow(pipes, cmap=cmap)
    plt.show()
    return

def count_filled(pipes: np.ndarray, filled: np.ndarray) -> int:
    count = 0
    it = np.nditer(pipes, flags=['multi_index'])
    for _ in it:
        pipe_y, pipe_x = it.multi_index
        pixel_x = pipe_x * 3
        pixel_y = pipe_y * 3
        all_filled = (filled[pixel_y:pixel_y+3, pixel_x:pixel_x+3] == FILLED).all()
        # print(pipe_x, pipe_y, all_filled)
        if all_filled:
            count += 1
    return count

def solve(lines: str):
    pipes = parse(lines)
    pipes = clean(pipes)
    start_pos, start_pipe_shape = calc_start_pipe_shape(pipes)
    pipes[start_pos] = start_pipe_shape
    x, y = start_pos
    # Get the start in "fillable" coordinates
    x = x * 3 + 1
    y = y * 3 + 1
    start_options = [
        (x - 1, y - 1),
        (x - 1, y + 1),
        (x + 1, y + 1),
        (x + 1, y - 1),
    ]
    for start_pos_fillable in start_options:
        pixels = pipes_to_fillable(pipes)
        success, pixels = fill(start_pos_fillable, pixels)
        if success:
            show_pipes(pixels)
            print(count_filled(pipes, pixels))
            break
    return

if __name__ == '__main__':
    solve(example1)
    solve(example2)
    solve(example3)
    solve(open('input.txt').read())
