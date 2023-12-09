from dataclasses import dataclass

import numpy as np

example = """Time:      7  15   30
Distance:  9  40  200
"""

@dataclass
class Race:
    time: int
    distance: int

    def play(self, hold_time: int) -> bool:
        travel_time = self.time - hold_time
        travel = travel_time * hold_time
        return travel > self.distance


def race_wins(race: Race) -> int:
    # There are bound to be many wins, so count losses from either end, then
    # consider the wins to be the time - the losses.
    losses = 0
    for hold_time in range(race.time):
        if not race.play(hold_time):
            losses += 1
        else:
            break
    for hold_time in reversed(range(race.time)):
        if not race.play(hold_time):
            losses += 1
        else:
            break
    return race.time - losses

def parse(s: str):
    time_line, distance_line = s.splitlines()
    _, time_line = time_line.replace(' ', '').split(':')
    _, distance_line = distance_line.replace(' ', '').split(':')
    race = Race(int(time_line), int(distance_line))
    return race

def solve(s: str):
    race = parse(s)
    print(race_wins(race))

if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
