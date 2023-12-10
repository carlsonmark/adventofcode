import re
from dataclasses import dataclass
from typing import Tuple, List
import numpy as np

# Start at all nodes that end in A.
# Follow the same path from each start node simultaneously.
# ... Reading comprehension problem... I initially thought it said to follow
#     all paths simultaneously for each node... whoops!
# Stop when all paths end in Z.
example = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

@dataclass
class Node:
    name: str
    L: str
    R: str
    is_end: bool


def parse_input(s: str) -> Tuple[str, dict]:
    lines = s.splitlines()
    lrs = lines[0]
    graph = {}
    for line in lines[2:]:
        match = re.match(r'(\w+) = \((\w+), (\w+)\)', line)
        node_name = match.group(1)
        left = match.group(2)
        right = match.group(3)
        graph[node_name] = Node(name=node_name, L=left, R=right, is_end=node_name.endswith('Z'))
    return lrs, graph

def start_nodes(graph: dict) -> List[Node]:
    return [graph[name] for name in graph if name.endswith('A')]

def solve(s: str):
    lrs, graph = parse_input(s)
    # After making this, I learned about itertools.cycle()
    def next_step():
        step_count = 0
        while True:
            yield step_count, lrs[step_count]
            step_count += 1
            if step_count >= len(lrs):
                step_count = 0
    step_generator = next_step()

    start = start_nodes(graph)
    repetitions = []
    # Find out when the cycle loops for each node
    for node in start:
        # All locations that have been visited already
        cache = set()
        for cycle_count, (sub_cycle_count, direction) in enumerate(step_generator, start=1):
            if direction == 'L':
                name = node.L
            else:
                name = node.R
            next_node = graph[name]
            key = (name, sub_cycle_count)
            cache.add(key)
            if next_node.is_end and key in cache:
                repetitions.append(cycle_count)
                break
            node = next_node
    print(repetitions)
    print(np.lcm.reduce(repetitions))


if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
