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
    maze: np.ndarray
    instructions: List[Tuple[str, int, int]]
    start: Tuple[int, int]

    @classmethod
    def from_str(cls, lines: str):
        instructions = []
        for line in lines.splitlines():
            direction, step_str, hex_str = line.split(' ')
            step = int(step_str)
            hex_code = int(hex_str[2:-1], 16)
            instructions.append((direction, step, hex_code))
        # Walk through the steps and see what the min/max is in both dimensions
        x = 0
        min_x = 0
        max_x = 0
        y = 0
        min_y = 0
        max_y = 0
        for direction, step, _ in instructions:
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
        width = max_x - min_x
        height = max_y - min_y
        start = (-min_y, -min_x)
        return Puzzle(np.zeros((height+1, width+1), dtype=int), instructions, start)

    def walk_steps(self):
        y, x = self.start
        for direction, step, _ in self.instructions:
            for _ in range(step):
                if direction == 'U':
                    y -= 1
                elif direction == 'D':
                    y += 1
                elif direction == 'R':
                    x += 1
                elif direction == 'L':
                    x -= 1
                self.maze[y, x] = 1
        return


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
    fillable[start_pos] = DUG
    try:
        options = set(find_empty(start_pos, fillable))
        while options:
            # Fill first
            for option in options:
                fillable[option] = DUG
            # Find new options for each filled position
            next_options = set()
            for option in options:
                for pos in find_empty(option, fillable):
                    next_options.add(pos)
            options = next_options
    except IndexError:
        success = False
    return success, fillable

def show_maze(maze):
    cmap_list = (
        # 0: Untouched
        (1, 1, 1, 1),
        # 1: Dug
        (0, 0, 0, 1),
    )
    cmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmap_list, 3)
    fig, ax = plt.subplots(1, 1)
    ax.imshow(maze, cmap=cmap)
    plt.show()
    return

def solve(lines: str):
    puzzle = Puzzle.from_str(lines)
    puzzle.walk_steps()
    success, maze = fill((puzzle.start[0]+1, puzzle.start[1]+1), puzzle.maze)
    # print(maze)
    print(sum(sum(maze)))
    show_maze(maze)
    return


if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
