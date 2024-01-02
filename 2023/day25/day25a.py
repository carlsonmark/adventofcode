from easygraph import Graph
from easygraph.functions.path.path import single_source_bfs

example = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

def parse(lines: str):
    connections = {}
    G = Graph()
    for line in lines.splitlines():
        key, rest = line.split(': ')
        components = set(rest.split(' '))
        if key in connections:
            connections[key].update(components)
        else:
            connections[key] = components
        for component in components:
            G.add_edge(key, component)
    return connections, G

def solve(lines: str):
    connections, G = parse(lines)
    print('digraph "connections" {')
    for key, values in connections.items():
        for value in values:
            print(f'{key} -- {value}')
    print('}')
    print()
    print('Put that in /tmp/graph.txt, then run:')
    print('neato -Tsvg /tmp/graph.txt -o /tmp/graph.svg')
    print('Then open it in a web browser to see which three to cut... '
          'It is tricky because the text overlaps still...')
    # Now, remove them and count the sizes of each group
    to_remove = (('lxt', 'lsv'),
                 ('qmr', 'ptj'),
                 ('dhn', 'xvh'))
    for left, right in to_remove:
        if not G.has_edge(left, right) and not G.has_edge(right, left):
            print('???', left, right)
        try:
            G.remove_edge(left, right)
            continue
        except KeyError: pass
        try:
            G.remove_edge(right, left)
        except KeyError: pass
    print(G.nodes)
    # It took an embarrassingly long amount of time to find this function.
    # It would have been faster to just write it myself, but I really wanted
    # to use at least one method from EasyGraph for AoC this year.
    left_count = len(single_source_bfs(G, left))
    right_count = len(single_source_bfs(G, right))
    print(f'{left_count=}, {right_count=} {left_count * right_count=}')
    return


if __name__ == '__main__':
    # solve(example)
    solve(open('input.txt').read())
