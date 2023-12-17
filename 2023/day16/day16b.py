# Same as before, but start at all outside positions and find the one that
# visits the most number of tiles

import dataclasses
from copy import deepcopy
from functools import lru_cache
from typing import Tuple, List

import numpy as np

example = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""

EMPTY = 0
MIRROR_SWNE = 1
MIRROR_NWSE = 2
SPLIT_V = 3
SPLIT_H = 4

VISITED_E = 1
VISITED_S = 2
VISITED_W = 4
VISITED_N = 8

@dataclasses.dataclass
class Puzzle:
    maze: np.ndarray
    visited: np.ndarray

    @classmethod
    def from_str(cls, lines: str):
        lines = lines.splitlines()
        nrows = len(lines)
        ncols = len(lines[0])
        maze = np.zeros((nrows, ncols), dtype=int)
        for i, row in enumerate(lines):
            for j, c in enumerate(row):
                if c == '/':
                    maze[i, j] = MIRROR_SWNE
                elif c == '\\':
                    maze[i, j] = MIRROR_NWSE
                elif c == '|':
                    maze[i, j] = SPLIT_V
                elif c == '-':
                    maze[i, j] = SPLIT_H
        return Puzzle(
            maze=maze,
            visited=np.zeros_like(maze)
        )

    def visit(self, row: int, col: int, direction: int) -> bool:
        was_visited = self.visited[row, col] & direction > 0
        self.visited[row, col] |= direction
        return was_visited

    def next_in_bounds(self, row: int, col: int, direction: int) -> List[Tuple[int, int, int]]:
        """
        Returns a position and direction if it would be in bounds still,
        otherwise an empty list is returned.
        """
        next_pos = []
        if direction == VISITED_N and row > 0:
            next_pos = (row - 1, col, direction)
        elif direction == VISITED_S and row < (self.maze.shape[0] - 1):
            next_pos = (row + 1, col, direction)
        elif direction == VISITED_W and col > 0:
            next_pos = (row, col - 1, direction)
        elif direction == VISITED_E and col < (self.maze.shape[1] - 1):
            next_pos = (row, col + 1, direction)
        return next_pos

def next_positions(row: int, col: int, direction: int, puzzle: Puzzle) -> List[Tuple[int, int, int]]:
    next_pos = []
    # What is this current location?
    current = puzzle.maze[row, col]
    if current == EMPTY:
        # Empty, continue in same direction
        next_pos.append(puzzle.next_in_bounds(row, col, direction))
    elif current == MIRROR_SWNE:
        # /
        # If travelling E->N, W->S, S->W, N->E
        if direction == VISITED_E:
            next_direction = VISITED_N
        elif direction == VISITED_W:
            next_direction = VISITED_S
        elif direction == VISITED_S:
            next_direction = VISITED_W
        else:
            next_direction = VISITED_E
        next_pos.append(puzzle.next_in_bounds(row, col, next_direction))
    elif current == MIRROR_NWSE:
        # \
        # If travelling E->S, W->N, S->E, N->W
        if direction == VISITED_E:
            next_direction = VISITED_S
        elif direction == VISITED_W:
            next_direction = VISITED_N
        elif direction == VISITED_S:
            next_direction = VISITED_E
        else:
            next_direction = VISITED_W
        next_pos.append(puzzle.next_in_bounds(row, col, next_direction))
    elif current == SPLIT_H:
        # -
        # If travelling S or N, then E+W, otherwise, continue in same direction
        if direction in (VISITED_S, VISITED_N):
            next_pos.append(puzzle.next_in_bounds(row, col, VISITED_E))
            next_pos.append(puzzle.next_in_bounds(row, col, VISITED_W))
        else:
            next_pos.append(puzzle.next_in_bounds(row, col, direction))
    elif current == SPLIT_V:
        # |
        # If travelling E or W, then N+S, otherwise, continue in same direction
        if direction in (VISITED_E, VISITED_W):
            next_pos.append(puzzle.next_in_bounds(row, col, VISITED_N))
            next_pos.append(puzzle.next_in_bounds(row, col, VISITED_S))
        else:
            next_pos.append(puzzle.next_in_bounds(row, col, direction))
    return next_pos

def move(row: int, col: int, direction: int, puzzle: Puzzle) -> List[Tuple[int, int, int]]:
    # Get the next positions for the current position
    next_pos = next_positions(row, col, direction, puzzle)
    if not next_pos:
        return []
    # Mark the new positions as visited
    keep_going = []
    for pos in next_pos:
        if not pos:
            continue
        row, col, direction = pos
        was_visited = puzzle.visit(row, col, direction)
        if not was_visited:
            keep_going.append((row, col, direction))
    return keep_going

def solve(lines: str):
    original = Puzzle.from_str(lines)
    maximum = 0
    rows, cols = original.maze.shape
    # Visit all rows from both sides
    for row in range(rows):
        maximum = max(maximum, solve_from_start(row, 0, VISITED_E, deepcopy(original)))
        maximum = max(maximum, solve_from_start(row, cols-1, VISITED_W, deepcopy(original)))
    # Visit all cols from both sides
    for col in range(cols):
        maximum = max(maximum, solve_from_start(0, col, VISITED_S, deepcopy(original)))
        maximum = max(maximum, solve_from_start(rows-1, col, VISITED_N, deepcopy(original)))
    print(maximum)

def solve_from_start(row: int, col: int, direction: int, puzzle: Puzzle) -> int:
    # print(f'starting from {row=}, {col=}, {direction=}')
    positions = [(row, col, direction)]
    puzzle.visit(*positions[0])
    while positions:
        new_positions = []
        for row, col, direction in positions:
            new_positions.extend(move(row, col, direction, puzzle))
        positions = new_positions
    return sum((puzzle.visited > 0).flatten())



if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
