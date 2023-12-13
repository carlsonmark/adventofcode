# Oh, dear deity. Why did I choose to use this as a learning opportunity
# with generators.

import dataclasses
from typing import List

import numpy as np

# Note: Always in the given order

example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


@dataclasses.dataclass
class Puzzle:
    required_plus_optional: np.ndarray
    required: np.ndarray
    groups: np.ndarray

    @classmethod
    def from_string(self, s: str):
        row_str, groups_str = s.split(' ')
        required_plus_optional = [int(c == '#') for c in row_str.replace('?', '#')]
        required = [int(c == '#') for c in row_str]
        groups = [int(i) for i in groups_str.split(',')]
        return Puzzle(
            np.array(required_plus_optional, dtype=int),
            np.array(required, dtype=int),
            np.array(groups, dtype=int))


    def generator(self):
        shifts = np.zeros_like(self.groups)
        iter_pos = 1
        while True:
            arrangement = self.to_arrangement(shifts)
            if self.in_bounds(arrangement):
                # print(f'yielding {arrangement=}')
                yield arrangement
                iter_pos = 1
            else:
                shifts[-iter_pos] = 0
                iter_pos += 1
            if iter_pos > self.groups.shape[0]:
                break
            shifts[-iter_pos] += 1
        return

    def in_bounds(self, arrangement):
        return arrangement[-1] + self.groups[-1] <= self.required.shape[-1]

    def to_arrangement(self, shifts):
        arrangement = []
        pos = 0
        for i, shift in enumerate(shifts):
            pos += shift
            arrangement.append(pos)
            pos += self.groups[i] + 1
        return arrangement

    def to_row(self, arrangement) -> np.ndarray:
        row = np.zeros_like(self.required)
        for position, size in zip(arrangement, self.groups):
            for c in range(size):
                row[position + c] = 1
        return row

    def is_valid(self, arrangement):
        if not self.in_bounds(arrangement):
            return False
        row = self.to_row(arrangement)
        # Ensure all required positions are filled
        if ((self.required - row) > 0).any():
            return False
        # Ensure only valid positions are filled
        if ((row - self.required_plus_optional) > 0).any():
            return False
        return True

def parse(lines: str) -> List[Puzzle]:
    return [Puzzle.from_string(line) for line in lines.splitlines()]

def combinations(puzzle: Puzzle):
    generator = puzzle.generator()
    arrangements = []
    for arrangement in generator:
        if puzzle.is_valid(arrangement):
            # print(f'Found one: {arrangement} for { puzzle}')
            arrangements.append(arrangement)
    return len(arrangements)

def solve(lines: str):
    puzzles = parse(lines)
    all_results = []
    for puzzle in puzzles:
        all_results.append(combinations(puzzle))
        print(f'Found {all_results[-1]} for {puzzle}')
    print(f'{all_results}')
    print(f'{np.sum(all_results)}')
    return

if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
