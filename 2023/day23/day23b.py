import dataclasses
from copy import deepcopy
from typing import Tuple, List, Dict, Set

import numpy as np

# What's the longest path?
# Can go up a slope, but not on a travelled step.

# Walk all valid paths... which is a lot, so compress the problem first.
# Had a funny bug where I was marking the end as visited, then not un-marking it
# so it would only be visited once!

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
SLOPE_E = -3
SLOPE_S = -5
charmap = {
    'S': START,
    '#': FOREST,
    '.': PATH,
    '>': SLOPE_E,
    'v': SLOPE_S,
}
inv_charmap = {v: k for k, v in charmap.items()}

@dataclasses.dataclass
class Node:
    position: Tuple[int, int]
    neighbours: List[Tuple[int, Tuple[int, int]]]  # distance, (row, col)

@dataclasses.dataclass
class WalkingState:
    position: Tuple[int, int]

def parse(lines: str):
    split = lines.splitlines()
    puzzle = np.empty((len(split), len(split[0])), dtype=int)
    for i, line in enumerate(split):
        for j, c in enumerate(line):
            puzzle[i, j] = charmap[c]
    return puzzle

def options(state: WalkingState, puzzle):
    current_tile = puzzle[state.position]
    row, col = state.position
    # If standing on a slope, the only option is to go that direction
    if current_tile == SLOPE_E:
        state.position = row, col + 1
        return [state]
    if current_tile == SLOPE_S:
        state.position = row + 1, col
        return [state]

    impassible = (START, FOREST)
    states = []
    all_possible = (
        (row - 1, col), # Up
        (row + 1, col), # Down
        (row, col - 1), # Left
        (row, col + 1)  # Right
    )
    # No need to copy the first option
    first = True
    for to_position in all_possible:
        try:
            to_tile = puzzle[to_position]
        except IndexError:
            continue
        if to_tile not in impassible and to_tile <= 0:
            if first:
                state.position = to_position
                states.append(state)
                first = False
            else:
                state = deepcopy(state)
                state.position = to_position
                states.append(state)
    return states

def find_nodes(puzzle: np.ndarray) -> Dict[Tuple[int, int], Node]:
    start = (0, 1)
    end = puzzle.shape[0] - 1, puzzle.shape[1] - 2
    nodes = {
        start: Node(start, []),
        end: Node(end, [])
    }
    # First, find the nodes
    rows, cols = puzzle.shape
    for row in range(rows):
        if row == 0 or row == rows - 1:
            continue
        for col in range(cols):
            if col == 0 or col == cols - 1:
                continue
            if puzzle[row, col] != PATH:
                # Only the path can be a node
                continue
            left = puzzle[row, col - 1]
            right = puzzle[row, col + 1]
            up = puzzle[row - 1, col]
            down = puzzle[row + 1, col]
            maybe_node = False
            if left in (FOREST, SLOPE_E) and right == SLOPE_E:
                maybe_node = True
            elif left == SLOPE_E and right in (FOREST, SLOPE_E):
                maybe_node = True
            if not maybe_node:
                continue
            is_node = False
            if up in (FOREST, SLOPE_S) and down == SLOPE_S:
                is_node = True
            elif up == SLOPE_S and down in (FOREST, SLOPE_S):
                is_node = True
            if is_node:
                nodes[(row, col)] = Node((row, col), [])
    return nodes

def print_puzzle(puzzle: np.ndarray):
    lines = ''
    for r in range(puzzle.shape[0]):
        for c in range(puzzle.shape[1]):
            lines += inv_charmap.get(puzzle[r,c], 'O')
        lines += '\n'
    print(lines)
    return

def find_nodes_from(from_node: Node, puzzle: np.ndarray, nodes: Dict[Tuple[int, int], Node]) -> List[Tuple[int, Tuple[int, int]]]:
    destinations = []
    start = from_node.position
    puzzle[start] = 1
    opts = options(WalkingState(start), puzzle)
    for option in opts:
        found_next = False
        step_count = 1
        while not found_next:
            step_count += 1
            puzzle[option.position] = 1
            options_ = options(WalkingState(option.position), puzzle)
            option = options_[0]
            if option.position in nodes:
                destinations.append((step_count, option.position))
                found_next = True
    return destinations

def compress(puzzle: np.ndarray):
    nodes = find_nodes(puzzle)
    for node in nodes.values():
        node.neighbours = find_nodes_from(node, np.copy(puzzle), nodes)
    # for k, v in nodes.items():
    #     print(k, v)
    # for k in sorted(nodes):
    #     print(k, list(sorted(nodes[k].neighbours)))
    # Checking if all the nodes are correct:
    # cp = np.copy(puzzle)
    # for pos in nodes:
    #     cp[pos] = 1
    # print_puzzle(cp)
    # Printing in graphviz format:
    # dot -Tps /tmp/graph.txt -o /tmp/graph.ps && evince /tmp/graph.ps
    # for k, v in nodes.items():
    #     print(f'"{k}"')
    #     for other in v.neighbours:
    #         print(f'"{k}" -> "{other[1]}" [label="{other[0]}"]')
    return nodes

class DeadEnd(Exception):
    pass

def find_longest(length: int, next_pos: Tuple[int, int], nodes: Dict[Tuple[int, int], Node], end: Tuple[int, int], visited: Set[Tuple[int, int]]):
    if next_pos in visited:
        return 0
    # Mark node as visited
    visited.add(next_pos)
    node = nodes[next_pos]
    longest = 0
    for neighbour_distance, neighbour_pos in node.neighbours:
        if neighbour_pos == end:
            # Done, at the end
            visited.remove(next_pos)
            return length + neighbour_distance
        if neighbour_pos not in nodes:
            # This one was removed already
            continue
        longest = max(longest,
                      find_longest(
                          length + neighbour_distance, neighbour_pos, nodes, end, visited
                      ))
    visited.remove(next_pos)
    return longest


def solve(lines: str):
    puzzle = parse(lines)
    nodes = compress(puzzle)
    start = (0, 1)
    end = puzzle.shape[0] - 1, puzzle.shape[1] - 2
    start_node = nodes.pop(start)
    start_neighbour = start_node.neighbours[0]
    print(find_longest(start_neighbour[0], start_neighbour[1], deepcopy(nodes), end, set()))
    return

if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
