# Same as before, but list is a range: start+len of seeds
# Note: Use pypy3 (a version that supports dataclasses) in order for this to
#       complete in a reasonable amount of time.

from copy import deepcopy
from multiprocessing import Pool
import dataclasses
import time
from typing import List, Tuple

example = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

def parse_ints(s) -> List[int]:
    return [int(n) for n in s.split(' ')]

@dataclasses.dataclass
class Lookup:
    destination_start: int
    source_start: int
    range_length: int

    def source_in_range(self, value: int) -> bool:
        return value >= self.source_start and value < self.source_start + self.range_length

    def map(self, value: int) -> int:
        if self.source_in_range(value):
            offset = self.source_start - self.destination_start
            return value - offset
        else:
            return -99999

@dataclasses.dataclass
class Maps:
    seed_range_list: List[Tuple[int, int]] = dataclasses.field(default_factory=list)
    s2s: List[Lookup] = dataclasses.field(default_factory=list)
    s2f: List[Lookup] = dataclasses.field(default_factory=list)
    f2w: List[Lookup] = dataclasses.field(default_factory=list)
    w2l: List[Lookup] = dataclasses.field(default_factory=list)
    l2t: List[Lookup] = dataclasses.field(default_factory=list)
    t2h: List[Lookup] = dataclasses.field(default_factory=list)
    h2l: List[Lookup] = dataclasses.field(default_factory=list)

    @classmethod
    def from_str(cls, lines: str):
        maps = Maps()
        list_to_parse = None
        for line in lines.splitlines():
            if not line:
                continue
            elif line.startswith('seeds'):
                interleaved = parse_ints(line.split(': ')[1])
                iterator = iter(interleaved)
                maps.seed_range_list = list(zip(iterator, iterator))
            elif line.startswith('seed-'):
                list_to_parse = maps.s2s
            elif line.startswith('soil-'):
                list_to_parse = maps.s2f
            elif line.startswith('fertilizer-'):
                list_to_parse = maps.f2w
            elif line.startswith('water-'):
                list_to_parse = maps.w2l
            elif line.startswith('light-'):
                list_to_parse = maps.l2t
            elif line.startswith('temperature-'):
                list_to_parse = maps.t2h
            elif line.startswith('humidity-'):
                list_to_parse = maps.h2l
            else:
                list_to_parse.append(Lookup(*parse_ints(line)))
        return maps

    def map_s2s(self, value: int) -> int:
        for list_ in self.s2s:
            possible = list_.map(value)
            if possible != -99999:
                return possible
        return value

    def map_s2f(self, value: int) -> int:
        for list_ in self.s2f:
            possible = list_.map(value)
            if possible != -99999:
                return possible
        return value

    def map_f2w(self, value: int) -> int:
        for list_ in self.f2w:
            possible = list_.map(value)
            if possible != -99999:
                return possible
        return value

    def map_w2l(self, value: int) -> int:
        for list_ in self.w2l:
            possible = list_.map(value)
            if possible != -99999:
                return possible
        return value

    def map_l2t(self, value: int) -> int:
        for list_ in self.l2t:
            possible = list_.map(value)
            if possible != -99999:
                return possible
        return value

    def map_t2h(self, value: int) -> int:
        for list_ in self.t2h:
            possible = list_.map(value)
            if possible != -99999:
                return possible
        return value

    def map_h2l(self, value: int) -> int:
        for list_ in self.h2l:
            possible = list_.map(value)
            if possible != -99999:
                return possible
        return value

    def location(self, seed: int) -> int:
        soil = self.map_s2s(seed)
        fertilizer = self.map_s2f(soil)
        water = self.map_f2w(fertilizer)
        light = self.map_w2l(water)
        temperature = self.map_l2t(light)
        humidity = self.map_t2h(temperature)
        location = self.map_h2l(humidity)
        # print(f'Seed {seed}, {soil=}, {fertilizer=}, {water=}, {light=}, {temperature=}, {humidity=}, {location=}')
        return location

    def lowest_location(self, seed_start: int, range_length: int) -> int:
        lowest = 1<<30  # If it's not lower than this, it's not going to be the lowest
        for seed in range(seed_start, seed_start + range_length):
            lowest = min(lowest, self.location(seed))
        return lowest

def lowest_for_seed_range(args):
    start = time.monotonic()
    maps, seed_range = args
    location = maps.lowest_location(*seed_range)
    print(f'{location=}, {time.monotonic() - start=}')
    return location

def solve(lines: str):
    maps = Maps.from_str(lines)
    arg_list = [(deepcopy(maps), l) for l in maps.seed_range_list]
    with Pool(8) as p:
        locations = p.map(lowest_for_seed_range, arg_list)

    print(f'{min(locations)=}')
    return

if __name__ == '__main__':
    solve(example)
    solve(open('day5input.txt').read())

"""
location=1073741824, time.monotonic() - start=6.944860816933215
location=1073741824, time.monotonic() - start=24.79112150799483
location=749391108, time.monotonic() - start=123.83007535431534
location=780711947, time.monotonic() - start=207.00915170833468
location=332248829, time.monotonic() - start=234.3155575497076
location=412475024, time.monotonic() - start=257.3052422143519
location=13286163, time.monotonic() - start=326.8474805559963
location=295741385, time.monotonic() - start=357.3073078645393
location=194991402, time.monotonic() - start=370.69808196555823
location=2008786, time.monotonic() - start=457.5953907314688
min(locations)=2008786 # too high
"""
