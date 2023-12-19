import dataclasses
from typing import Tuple, List

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

example = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

EMPTY = 0
DUG = 1


@dataclasses.dataclass
class Puzzle:
    vertices: np.ndarray
    instructions: List[Tuple[str, int]]
    circumference: int

    @classmethod
    def from_str(cls, lines: str):
        instructions = []
        for line in lines.splitlines():
            _, _, hex_str = line.split(' ')
            step = int(hex_str[2:-2], 16)
            direction_str = hex_str[-2]
            if direction_str == '0':
                direction = 'R'
            elif direction_str == '1':
                direction = 'D'
            elif direction_str == '2':
                direction = 'L'
            else:
                direction = 'U'
            instructions.append((direction, step))
        return Puzzle(np.zeros((len(instructions), 4), dtype=int), instructions, 0)

    def walk_steps(self):
        y, x = 0, 0
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for i, (direction, step) in enumerate(self.instructions):
            self.vertices[i][:2] = [y, x]
            if direction == 'U':
                y -= step
            elif direction == 'D':
                y += step
            elif direction == 'R':
                x += step
            elif direction == 'L':
                x -= step
            min_x = min(x, min_x)
            max_x = max(x, max_x)
            min_y = min(y, min_y)
            max_y = max(y, max_y)
            self.vertices[i][2:] = [y, x]
            self.circumference += step
        return

# Stolen from stack overflow: Calculate internal area from vertices
# using Shoelace formula. https://stackoverflow.com/a/30408825
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def solve(lines: str):
    puzzle = Puzzle.from_str(lines)
    puzzle.walk_steps()
    internal_area = PolyArea(puzzle.vertices[:,1],
                   puzzle.vertices[:,0])
    total_area = internal_area + puzzle.circumference / 2 + 1
    print(f'{total_area=}')
    return


if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
