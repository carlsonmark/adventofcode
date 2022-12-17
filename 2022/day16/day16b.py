# Notes
# Would it be faster to take 4 minutes off the top and have two paths followed at once?
# Plan:
# Run it twice and add both score
# Second run: Have the best visited set populated from the previous run
# This is not a real solution, since it fails for small graphs where you can open all the valves very easily

import re
import pprint
from easygraph import Graph
from easygraph.functions.path import single_source_dijkstra

test_input = """\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""


def parse_input(s: str):
    graph = Graph()
    valves_of_interest = []
    flow_rates = {}
    for line in s.splitlines(keepends=False):
        match = re.match(r'Valve (\w+) has flow rate=(\d+); tunnel lead to valve (.*)', line.replace('tunnels', 'tunnel').replace('leads', 'lead').replace('valves', 'valve'))
        valve_name = match.group(1)
        flow_rate = int(match.group(2))
        tunnels = match.group(3).split(', ')
        graph.add_node(valve_name, flow_rate=flow_rate, tunnels=tunnels)
        if flow_rate > 0:
            valves_of_interest.append(valve_name)
            flow_rates[valve_name] = flow_rate
    for node_name, node in graph.nodes.items():
        for tunnel in node['tunnels']:
            graph.add_edge(node_name, tunnel)
    return graph, valves_of_interest, flow_rates


def find_shortest_paths_for(valve, graph, valves_of_interest):
    distances = {}
    for dest_valve in valves_of_interest:
        distances[dest_valve] = single_source_dijkstra(graph, valve, target=dest_valve)[dest_valve]
    return distances


def potential_score(distances, start, valve, time_remaining, flow_rates):
    distance = distances[start][valve]
    score = (time_remaining - distance - 1) * flow_rates[valve]
    return score


def walk_graph(path, distances, start, valves_of_interest, flow_rates, time_remaining=26):
    if time_remaining < 0:
        return 0
    scores = []
    for valve in valves_of_interest:
        if valve in path:
            continue
        # See what the score would be if we travelled to that graph
        score = potential_score(distances, start, valve, time_remaining, flow_rates)
        if score > 0:
            scores.append((score, valve))
    # Travel to each one, in order of most likely to be good
    best_score = 0
    # Just for fun, try limiting the number of locations to just a few of the best options
    scores = scores[:10]
    best_sub_path = []
    for score, valve in reversed(sorted(scores)):
        path.add(valve)
        distance = distances[start][valve]
        sub_score, sub_path = walk_graph(path, distances, valve, valves_of_interest, flow_rates, time_remaining - distance - 1)
        sub_score = sub_score + score
        if sub_score > best_score:
            best_score = sub_score
            best_sub_path = sub_path
            best_sub_path.append(valve)
        # if start == 'AA':
        #     print(best_score, valve)
        #     print(best_sub_path)
        path.remove(valve)
    return best_score, best_sub_path


start_ = 'AA'
graph_, valves_of_interest_, flow_rates_ = parse_input(test_input)
distances_ = {}
for valve_ in [start_, *valves_of_interest_]:
    distances_[valve_] = find_shortest_paths_for(valve_, graph_, valves_of_interest_)

path_ = set()
score_1, best_path = walk_graph(path_, distances_, start_, valves_of_interest_, flow_rates_)
print(score_1)
path_ = set(best_path)
score_2, best_path_2 = walk_graph(path_, distances_, start_, valves_of_interest_, flow_rates_)
print(f'{score_1} + {score_2} = {score_1 + score_2}')


start_ = 'AA'
graph_, valves_of_interest_, flow_rates_ = parse_input(open('day16-input.txt').read())
distances_ = {}
for valve_ in [start_, *valves_of_interest_]:
    distances_[valve_] = find_shortest_paths_for(valve_, graph_, valves_of_interest_)
    pprint.pprint(distances_[valve_])

path_ = set()
score_1, best_path = walk_graph(path_, distances_, start_, valves_of_interest_, flow_rates_)
print(score_1)
path_ = set(best_path)
score_2, best_path_2 = walk_graph(path_, distances_, start_, valves_of_interest_, flow_rates_)
print(f'{score_1} + {score_2} = {score_1 + score_2}')
