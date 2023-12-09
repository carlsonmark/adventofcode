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
    wins = 0
    for hold_time in range(race.time):
        if race.play(hold_time):
            wins += 1
    return wins

def parse(s: str):
    time_line, distance_line = s.splitlines()
    _, time_line = time_line.split(':')
    _, distance_line = distance_line.split(':')
    times = [
            int(v) for v in time_line.split(' ') if v
        ]
    distances = [
            int(v) for v in distance_line.split(' ') if v
        ]
    races = [Race(time, distance) for time, distance in list(zip(times, distances))]
    return races

def solve(s: str):
    races = parse(s)
    all_wins = [race_wins(race) for race in races]
    print(all_wins, np.product(all_wins))

if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
