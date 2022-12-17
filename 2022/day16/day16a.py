# Notes
# Trying to release pressure before a volcano erupts
# 30 mins, takes 1 min to turn a valve, 1 min to move to the next
# Once a valve is open it releases pressure steadily per minute
# Trying to maximize the amount of pressure released over the 30 mins
# Can start at any valve
# Do not have to open a valve once there
# It takes a minute to go to the first valve, no matter which one it is? So it's really 29 mins.
# Example shows a list of valve names that are open each minute, so maybe that is a hint as to an optimal implementation
# Plan:
# Dijkstra? With the edge length being the (inverse?) opportunity cost of not taking the path?
# I guess the end is not known, because the input data has more valves than minutes to turn them all
# What I really want to know is that for any given edge at any given time, what is the maximum amount of pressure
# I can release in the remaining time? Then just follow the edges that are the highest.
# What about walking it backward, will that make the weighting easier?
# Rethinking:
# Only consider moving to valves that are still closed, don't visit everything
# Rank options based on how much it would contribute to the total score if you went right there from where you are
# Try each one
# After moving, recompute all the potential score contributions
# Continue until the time has run out (and/or out of movement options)
# OK, scrap all that:
# Do not consider moving to valves with zero flow rates
# Find shortest path from AA to all vales under consideration
# For each of those valves, find the shortest path to all other vales under consideration
# Walk this new graph, starting from AA
# - It may be faster to sort options based on how much flow rate the valve has remaining


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


def walk_graph(path, distances, start, valves_of_interest, flow_rates, time_remaining=30):
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
    for score, valve in reversed(sorted(scores)):
        path.add(valve)
        distance = distances[start][valve]
        sub_score = score + walk_graph(path, distances, valve, valves_of_interest, flow_rates, time_remaining - distance - 1)
        best_score = max(sub_score, best_score)
        if start == 'AA':
            print(best_score, valve)
        path.remove(valve)
    return best_score


start_ = 'AA'
graph_, valves_of_interest_, flow_rates_ = parse_input(test_input)
distances_ = {}
for valve_ in [start_, *valves_of_interest_]:
    distances_[valve_] = find_shortest_paths_for(valve_, graph_, valves_of_interest_)

path_ = set()
score_ = walk_graph(path_, distances_, start_, valves_of_interest_, flow_rates_)
print(score_)


start_ = 'AA'
graph_, valves_of_interest_, flow_rates_ = parse_input(open('day16-input.txt').read())
distances_ = {}
for valve_ in [start_, *valves_of_interest_]:
    distances_[valve_] = find_shortest_paths_for(valve_, graph_, valves_of_interest_)
    pprint.pprint(distances_[valve_])

path_ = set()
score_ = walk_graph(path_, distances_, start_, valves_of_interest_, flow_rates_)
print(score_)
