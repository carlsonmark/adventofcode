
"""
in each game you played, what is the fewest number of cubes of each color that
could have been in the bag to make the game possible?
"""

import dataclasses
from typing import List

from plotly.serializers import np

example = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
# Games 1, 2, and 5 are valid
# Sum of valid ids: 8


@dataclasses.dataclass
class Step:
    blue: int
    green: int
    red: int


@dataclasses.dataclass
class Game:
    id: int
    steps: List[Step]

    def fewest_cubes_power(self) -> int:
        max_blues = max([step.blue for step in self.steps])
        max_greens = max([step.green for step in self.steps])
        max_reds = max([step.red for step in self.steps])
        return np.product([max_blues, max_greens, max_reds])


def parse_game(line):
    game_str, steps_str = line.split(': ')
    game = int(game_str.replace('Game ', ''))
    steps = []
    for step_str in steps_str.split('; '):
        blue = 0
        green = 0
        red = 0
        for num_and_colors in step_str.split(', '):
            num_str, color = num_and_colors.split(' ')
            num = int(num_str)
            if color == 'blue':
                blue = num
            elif color == 'green':
                green = num
            else:
                red = num
        steps.append(Step(blue, green, red))
    return Game(game, steps)


def solve(lines: str):
    games = [parse_game(line) for line in lines.splitlines()]
    return sum([game.fewest_cubes_power() for game in games])


if __name__ == '__main__':
    print(solve(example))
    print(solve(open('day2input.txt').read()))
