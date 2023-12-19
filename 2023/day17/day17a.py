import dataclasses
import heapq
import math
from copy import copy
from typing import Tuple, Iterator, Dict, List

import numpy as np

# Get from top left to bottom right, losing as little heat as possible,
# but also not going the same direction 3 steps in a row.
# Used @mebeim's code as a reference for the djikstra part, but the node
# related stuff is mine (and likely way more inefficient!)

example = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

example1 = """\
199999
199999
111111
"""

example2 = """\
111119999
999919999
999911111
"""

def parse(lines: str):
    split = lines.splitlines()
    maze = np.empty((len(split), len(split[0])), dtype=int)
    for i, line in enumerate(split):
        maze[i] = list(map(int, line))
    return maze

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

@dataclasses.dataclass(frozen=True, order=True)
class Node:
    y: int
    x: int
    direction: int
    count: int

    def grid_coords(self) -> Tuple[int, int]:
        return self.y, self.x

    def __iter__(self):
        yield self.y
        yield self.x
        yield self.direction
        yield self.count
        return


def in_bounds(bounds: Tuple[int, int], coords: Tuple[int, int]):
    return 0 <= coords[0] < bounds[0] and 0 <= coords[1] < bounds[1]


def direction_to_coords(direction: int, y: int, x: int) -> Tuple[int, int]:
    if direction == UP:
        return y+1, x
    if direction == DOWN:
        return y-1, x
    if direction == RIGHT:
        return y, x-1
    # LEFT
    return y, x+1

base_possible_directions = {
    UP: [LEFT, RIGHT],
    DOWN: [LEFT, RIGHT],
    LEFT: [UP, DOWN],
    RIGHT: [UP, DOWN],
}

def next_nodes(maze: np.ndarray, node: Node) -> Iterator[Tuple[Node, int]]:
    y, x = node.grid_coords()
    # Restrict to 90 degree turns
    possible_directions = copy(base_possible_directions[node.direction])
    # Restrict to 3 in the same direction
    if node.count < 2:
        possible_directions.append(node.direction)
    for possible_direction in possible_directions:
        next_coords = direction_to_coords(possible_direction, *node.grid_coords())
        if in_bounds(maze.shape, next_coords):
            count = 0
            if possible_direction == node.direction:
                count = node.count + 1
            yield Node(*next_coords, possible_direction, count), maze[next_coords]
    return

def walk_back(shortest_path: Dict[Node, Node], node: Node, source: Tuple[int, int]):
    path = []
    while node in shortest_path:
        path.append(node)
        node = shortest_path[node]
        if node.grid_coords() == source:
            break

    return path

def dijkstra(maze: np.ndarray,
             source: Tuple[int, int],
             destination: Tuple[int, int]):
    # Keep track of visited nodes
    visited = set()
    # Nodes to visit
    queue = [
        (0, Node(*source, RIGHT, 0)),
        (0, Node(*source, DOWN, 0)),
    ]
    shortest_path = {}
    # Node: Heat Loss
    results = {}
    # Continue as long as there are nodes to visit
    while queue:
        # Get the next nearest node
        distance, node = heapq.heappop(queue)
        # Is it the end?
        if node.grid_coords() == destination:
            return distance, walk_back(shortest_path, node, source)
        # Check if this one is already visited
        if node in visited:
            continue
        # Mark this one as visited
        visited.add(node)
        # For each node from here:
        for next_node, heat_loss in next_nodes(maze, node):
            # Get the heat for the path to this node:
            heat_loss += distance
            # See if this is better than the last time this node was visited
            prev_best = results.get(next_node, math.inf)
            if heat_loss < prev_best:
                results[next_node] = heat_loss
                shortest_path[next_node] = node
                heapq.heappush(queue, (heat_loss, next_node))
    return None


direction_map = {
    UP: '^',
    DOWN: 'V',
    LEFT: '<',
    RIGHT: '>'
}

def print_walked_maze(maze, path: List[Node]):
    cmaze = np.chararray(maze.shape)
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            cmaze[i,j] = str(maze[i, j])
    for node in path:
        cmaze[node.grid_coords()] = direction_map[node.direction]
    for i in range(cmaze.shape[0]):
        for j in range(cmaze.shape[1]):
            print(cmaze[i,j].decode(), end='')
        print()
    return

def solve(lines: str):
    maze = parse(lines)
    heat, path = dijkstra(maze, (0,0), (maze.shape[0]-1, maze.shape[1]-1))
    print_walked_maze(maze, path)
    print(f'{heat=}')
    return

if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
