# Walk along pipes and count distance, what is the furthest point on the loop?
# Should be the loop length / 2?
from enum import IntEnum
from typing import Tuple, Optional

import numpy as np

# Distance: 4
example1 = """.....
.S-7.
.|.|.
.L-J.
.....
"""

# Distance: 8
example2 = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

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

def parse(lines: str):
    split = lines.splitlines()
    pipes = np.zeros((len(split), len(split[0])), dtype=int)
    for line_no, line in enumerate(lines.splitlines()):
        pipes[line_no] = [Pipe.from_char(c) for c in line]
    return pipes

def solve(lines: str):
    pipes = parse(lines)
    start_pos = tuple(np.argwhere(pipes == Pipe.Start)[0])
    step_count = 1
    current_pos = next_pos(start_pos, start_pos, pipes)
    prev_pos = start_pos
    while current_pos is not None:
        step_count += 1
        next_step_pos = next_pos(current_pos, prev_pos, pipes)
        prev_pos = current_pos
        current_pos = next_step_pos
    print(f'{start_pos=}')
    print(f'{step_count=}, {step_count/2=}')
    return

if __name__ == '__main__':
    solve(example1)
    solve(example2)
    solve(open('input.txt').read())
