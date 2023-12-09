# Lists all the seeds that need to be planted.
# Lists:
# - What type of soil to use with each kind of seed
# - What type of fertilizer to use with each kind of soil
# - What type of water to use with each kind of fertilizer, etc.
# Lists contain ranges: Destination start, source start, range length
import dataclasses
from typing import List, Optional

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
        return value >= self.source_start and value <= self.source_start + self.range_length

    def map(self, value: int) -> Optional[int]:
        if self.source_in_range(value):
            offset = self.source_start - self.destination_start
            return value - offset
        else:
            return None

@dataclasses.dataclass
class Maps:
    seeds: List[int] = dataclasses.field(default_factory=list)
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
                maps.seeds = parse_ints(line.split(': ')[1])
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

    def map_which(self, which: str, value: int) -> int:
        for list_ in getattr(self, which):
            possible = list_.map(value)
            if possible is not None:
                return possible
        return value

def solve(lines: str):
    maps = Maps.from_str(lines)
    locations = []
    for seed in maps.seeds:
        soil = maps.map_which('s2s', seed)
        fertilizer = maps.map_which('s2f', soil)
        water = maps.map_which('f2w', fertilizer)
        light = maps.map_which('w2l', water)
        temperature = maps.map_which('l2t', light)
        humidity = maps.map_which('t2h', temperature)
        location = maps.map_which('h2l', humidity)
        locations.append(location)
        print(f'Seed {seed}, {soil=}, {fertilizer=}, {water=}, {light=}, {temperature=}, {humidity=}, {location=}')
    print(f'{min(locations)=}')
    return

if __name__ == '__main__':
    solve(example)
    solve(open('day5input.txt').read())
