# Requires `pip3 install Python-EasyGraph`

import re
from typing import Tuple

import easygraph as eg

# Follow left/right and count steps

example1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

example2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

# Graph is unnecessary, just used it to refresh myself on it from last year
def parse_input(s: str) -> Tuple[str, eg.Graph]:
    lines = s.splitlines()
    lrs = lines[0]
    graph = eg.Graph()
    for line in lines[2:]:
        match = re.match(r'(\w+) = \((\w+), (\w+)\)', line)
        node_name = match.group(1)
        left = match.group(2)
        right = match.group(3)
        graph.add_node(node_name, L=left, R=right)
    for node_name, node in graph.nodes.items():
        graph.add_edge(node_name, node['L'])
        graph.add_edge(node_name, node['R'])
    return lrs, graph

def solve(s: str):
    lrs, graph = parse_input(s)
    def next_step():
        step_count = 0
        while True:
            yield lrs[step_count]
            step_count += 1
            if step_count >= len(lrs):
                step_count = 0
    step_generator = next_step()
    current_node_name = 'AAA'
    step_count = 0
    while current_node_name != 'ZZZ':
        step_count += 1
        which = next(step_generator)
        node = graph.nodes[current_node_name]
        current_node_name = node[which]
    print(step_count)


if __name__ == '__main__':
    solve(example1)
    solve(example2)
    solve(open('input.txt').read())
