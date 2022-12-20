# Notes
# Build robots, collect resources
# Can only build one bot per turn
# Goal is to collect as much obsidian as possible
# It may be OK to assume that it is always a good idea to build an obsidian bot when possible
# Do not consider building other bots if we can collect the max amount of a resource type needed for any one bot
import re
from copy import deepcopy
from dataclasses import dataclass
from typing import Tuple

test_input = """\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""


@dataclass
class Blueprint:
    id_: int
    rb_ore_cost: Tuple[int, int]
    rb_clay_cost: Tuple[int, int]
    rb_obsidian_cost: Tuple[int, int]
    rb_geode_cost: Tuple[int, int]
    max_ore_cost: int=0

    def __post_init__(self):
        rb_ore, _ = self.rb_ore_cost
        clay_ore, _ = self.rb_clay_cost
        obsidian_ore, _ = self.rb_obsidian_cost
        geode_ore, _ = self.rb_geode_cost
        self.max_ore_cost = max(rb_ore, clay_ore, obsidian_ore, geode_ore)
        return


@dataclass
class GameState:
    time_remaining: int=32
    rb_ore: int=1
    rb_clay: int=0
    rb_obsidian: int=0
    rb_geode: int=0
    ore: int=1
    clay: int=0
    obsidian: int=0
    geode: int=0
    best_score: int=0
    new_rb_ore: int=0
    new_rb_clay: int=0
    new_rb_obsidian: int=0
    new_rb_geode: int=0

    def collect_resources(self):
        self.ore += self.rb_ore
        self.clay += self.rb_clay
        self.obsidian += self.rb_obsidian
        self.geode += self.rb_geode
        self.rb_ore += self.new_rb_ore
        self.rb_clay += self.new_rb_clay
        self.rb_obsidian += self.new_rb_obsidian
        self.rb_geode += self.new_rb_geode
        self.new_rb_ore = 0
        self.new_rb_clay = 0
        self.new_rb_obsidian = 0
        self.new_rb_geode = 0
        return

    def build_ore_robot(self, blueprint: Blueprint):
        ore, clay = blueprint.rb_ore_cost
        self.ore -= ore
        self.clay -= clay
        self.new_rb_ore = 1
        return

    def build_clay_robot(self, blueprint: Blueprint):
        ore, clay = blueprint.rb_clay_cost
        self.ore -= ore
        self.clay -= clay
        self.new_rb_clay = 1
        return

    def build_obsidian_robot(self, blueprint: Blueprint):
        ore, clay = blueprint.rb_obsidian_cost
        self.ore -= ore
        self.clay -= clay
        self.new_rb_obsidian = 1
        return

    def build_geode_robot(self, blueprint: Blueprint):
        ore, obsidian = blueprint.rb_geode_cost
        self.ore -= ore
        self.obsidian -= obsidian
        self.new_rb_geode = 1
        return

    def build_none_robot(self, _):
        return

    def try_build_robot(self, option: str, blueprint):
        getattr(self, f'build_{option}_robot')(blueprint)
        assert self.ore >= 0 and self.clay >= 0 and self.obsidian >= 0, f'Tried to build {option}, {self}'
        return


def parse_input(s: str):
    blueprints = []
    for line in s.splitlines(keepends=False):
        match = re.match(r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.', line)
        blueprint = Blueprint(
            id_=int(match.group(1)),
            rb_ore_cost=(int(match.group(2)), 0),
            rb_clay_cost=(int(match.group(3)), 0),
            rb_obsidian_cost=(int(match.group(4)), int(match.group(5))),
            rb_geode_cost=(int(match.group(6)), int(match.group(7))),
        )
        blueprints.append(blueprint)
    return blueprints


def robot_options(blueprint: Blueprint, state: GameState):
    options = set()
    # Build a geode robot, if it is possible (not necessarily the best solution)
    # How many resources needed to get a geode robot?
    geode_ore_needed, geode_obsidian_needed = blueprint.rb_geode_cost
    geode_ore_needed -= state.ore
    geode_obsidian_needed -= state.obsidian
    if geode_obsidian_needed <= 0 and geode_ore_needed <= 0:
        options.add('geode')

    # Probably build an obsidian robot if it is possible
    # How many resources needed to get an obsidian robot?
    obsidian_ore_needed, obsidian_clay_needed = blueprint.rb_obsidian_cost
    obsidian_ore_needed -= state.ore
    obsidian_clay_needed -= state.clay
    if obsidian_clay_needed <= 0 and obsidian_ore_needed <= 0:
        options.add('obsidian')

    # Ditto for clay robot
    clay_ore_needed, _ = blueprint.rb_clay_cost
    clay_ore_needed -= state.ore
    clay_robot_needed = False
    if clay_ore_needed <= 0 and state.time_remaining > 3:
        clay_robot_needed = True

    # Is another clay robot needed?
    # Only if:
    # - More obsidian robots are needed
    # - The amount of clay gathered per turn is < the amount of clay to make an obsidian robot
    obsidian_robot_needed = state.rb_obsidian < blueprint.rb_geode_cost[1]
    clay_robot_needed &= obsidian_robot_needed
    clay_robot_needed &= state.rb_clay < blueprint.rb_obsidian_cost[1]

    if clay_robot_needed:
        clay_ore_cost, _ = blueprint.rb_clay_cost
        if clay_ore_cost - state.ore <= 0:
            if state.rb_clay == 0:
                options = {'clay'}
            else:
                options.add('clay')

    # Is another ore robot needed?
    # Only if the amount of ore gathered per turn is < the amount to make other robots
    x = state.rb_ore
    y = state.ore
    t = state.time_remaining + 1
    z = blueprint.max_ore_cost
    ore_robot_needed = x * t + y < t * z
    # ore_robot_needed = state.rb_ore < blueprint.max_ore_cost

    if ore_robot_needed:
        ore_ore_cost, _ = blueprint.rb_ore_cost
        if ore_ore_cost <= state.ore:
            options.add('ore')

    options.add('none')
    return options


def find_optimal(blueprint: Blueprint, state: GameState, skipped_options):
    state.time_remaining -= 1
    # if state.time_remaining == 0:
    #     state.best_score = state.geode + state.rb_geode
    #     return state
    if state.time_remaining == 1:
        state.best_score = state.geode + state.rb_geode
        return state
    options = robot_options(blueprint, state)
    for option in skipped_options:
        if option in options:
            options.remove(option)
    best_score = state.best_score
    best_state = state
    for option in options:
        option_state = GameState(**vars(state))
        option_state.try_build_robot(option, blueprint)
        option_state.collect_resources()
        # If this option is 'none', and there are other options, don't build those other options
        # until a different robot was built.
        # They were skipped for a reason, not just to hold off on building them.
        skipped_options = set()
        if option == 'none':
            skipped_options = options.copy()
            skipped_options.remove('none')
        option_state = find_optimal(blueprint, option_state, skipped_options)
        if option_state.best_score > best_score:
            best_score = option_state.best_score
            best_state = option_state
    return best_state


def compute_quality_level(blueprint: Blueprint):
    state = GameState()
    state = find_optimal(blueprint, state, set())
    quality = blueprint.id_ * state.best_score
    return quality, state

from multiprocessing import Pool

blueprints_ = parse_input(test_input)
# quality_, state_ = compute_quality_level(blueprints_[0])
# print(quality_, state_)
# quality_, state_ = compute_quality_level(blueprints_[1])
# print(quality_, state_)

with Pool(2) as p:
    results = p.map(compute_quality_level, blueprints_)
    for i, qs in enumerate(results):
        q, s = qs
        bp = blueprints_[i]
        print(f'{bp.id_}, {q=}, {s}')

blueprints_ = parse_input(open('day19-input.txt').read())
# sum_qualities = 0
# for blueprint_ in blueprints_:
#     quality_, state = compute_quality_level(blueprint_)
#     sum_qualities += quality_
#     print(f'{blueprint_.id_}, {quality_=} sum: {sum_qualities}, {state}')
#

with Pool(3) as p:
    results = p.map(compute_quality_level, blueprints_[:3])
    geodes = []
    for i, qs in enumerate(results):
        q, s = qs
        bp = blueprints_[i]
        geodes.append(s.best_score)
        print(f'{bp.id_}, {s}')

    prod = geodes[0] * geodes[1] * geodes[2]
    print(f'{prod=}, {geodes=}')
