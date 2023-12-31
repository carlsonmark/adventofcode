import dataclasses
from copy import deepcopy
from typing import Tuple

import numpy as np

# What's the longest path?
# Can not go up a slope or go back on a travelled step.

# Walk all valid paths.
# If a path ends at the end, record how long it is.

example = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

START = -999
FOREST = -1
PATH = 0
SLOPE_N = -2
SLOPE_E = -3
SLOPE_W = -4
SLOPE_S = -5
charmap = {
    'S': START,
    '#': FOREST,
    '.': PATH,
    '^': SLOPE_N,
    '>': SLOPE_E,
    '<': SLOPE_W,
    'v': SLOPE_S,
}
inv_charmap = {v: k for k, v in charmap.items()}

def parse(lines: str):
    split = lines.splitlines()
    puzzle = np.empty((len(split), len(split[0])), dtype=int)
    for i, line in enumerate(split):
        for j, c in enumerate(line):
            puzzle[i, j] = charmap[c]
    return puzzle

def print_puzzle(puzzle: np.ndarray):
    lines = ''
    for r in range(puzzle.shape[0]):
        for c in range(puzzle.shape[1]):
            lines += inv_charmap.get(puzzle[r,c], 'O')
        lines += '\n'
    print(lines)
    return

@dataclasses.dataclass
class WalkingState:
    puzzle: np.ndarray
    position: Tuple[int, int]
    step_count: int=0


def options(state: WalkingState):
    current_tile = state.puzzle[state.position]
    row, col = state.position
    # If standing on a slope, the only option is to go that direction
    if current_tile == SLOPE_N:
        state.position = row - 1, col
        return [state]
    if current_tile == SLOPE_E:
        state.position = row, col + 1
        return [state]
    if current_tile == SLOPE_W:
        state.position = row, col - 1
        return [state]
    if current_tile == SLOPE_S:
        state.position = row + 1, col
        return [state]

    states = []
    all_possible = (
        ((PATH, SLOPE_N), (row - 1, col)), # Up
        ((PATH, SLOPE_S), (row + 1, col)), # Down
        ((PATH, SLOPE_W), (row, col - 1)), # Left
        ((PATH, SLOPE_E), (row, col + 1))  # Right
    )
    # No need to copy the first option
    first = True
    for ok_to, to_position in all_possible:
        to_tile = state.puzzle[to_position]
        if to_tile in ok_to:
            if first:
                state.position = to_position
                states.append(state)
                first = False
            else:
                state = deepcopy(state)
                state.position = to_position
                states.append(state)
    return states


def solve(lines: str):
    puzzle = parse(lines)
    start = (0, 1)
    puzzle[start] = START
    end = puzzle.shape[0] - 1, puzzle.shape[1] - 2
    states = [WalkingState(puzzle, start)]
    end_states = []
    while states:
        next_states = []
        for state in states:
            opts = options(state)
            for option in opts:
                option.step_count += 1
                state.puzzle[option.position] = option.step_count
                if option.position == end:
                    end_states.append(option)
                else:
                    next_states.append(option)
            # print_puzzle(state.puzzle)
        states = next_states
    longest = 0
    for state in end_states:
        longest = max(longest, state.step_count)
    print(f'{longest=}')
    return

if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
