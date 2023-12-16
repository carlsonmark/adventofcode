"""
Using part 1 was a non-starter for part 2
- Impossible to generate that many combinations and check them all
First attempt at a re-write was a disaster as well
- Using numpy arrays was more cumbersome than it was worth
- I was keeping two lists of "mandatory" and "mandatory plus optional" positions
  which was extremely awkward to work with when it came to recursion
- I kept getting stuck with either returning 0 when faced with an initial '.'
  or double-counting combinations
Gave up and looked for inspiration on reddit. Found an excellent write-up by
/u/xavdid, here: https://advent-of-code.xavd.id/writeups/2023/day/12/
The main things I was missing were:
- I had been considering '?' to be effectively '#', then making sure that all
  '#' were used correctly, which was way too difficult
- Instead, considering '?' to be both '.' and '#' made way more sense
- Then, all you have to do for '#' use checking is:
  - Make sure there are no more '#' when you are finished with the groups
  - Make sure that there is no '#' at the end of a group (if there are remaining
    characters)
"""

import dataclasses
from functools import lru_cache
from typing import Tuple

example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

@dataclasses.dataclass
class Puzzle:
    row: str
    groups: Tuple[int]

    @classmethod
    def from_string(cls, s: str):
        row_str, groups_str = s.split(' ')
        # Simplify row_str by collapsing all '..' into '.'
        try:
            while row_str.index('..'):
                row_str = row_str.replace('..', '.')
        except ValueError:
            pass
        row_str = '?'.join([row_str]*5)
        groups_str = ','.join([groups_str]*5)
        groups = tuple([int(i) for i in groups_str.split(',')])
        return Puzzle(
            row_str,
            groups)


@lru_cache(None)
def valid_combinations(row: str, groups: Tuple[int]) -> int:
    if not row:
        if groups:
            # There are still groups left and nothing to do with them
            return 0
        return 1
    if not groups:
        if '#' in row:
            # A mandatory character is unused!
            return 0
        return 1
    first, rest = row[0], row[1:]
    if first == '.':
        # Ignore the empty space
        return valid_combinations(rest, groups)
    if first == '#':
        # See if the next group matches
        group = groups[0]
        # Make sure there is enough data left for the group
        if len(row) < group:
            return 0
        # Special case: If the next character after the end of the group
        #               is '#', then it this combo is invalid.
        if len(row) > group and row[group] == '#':
            return 0
        # Normal case: If there are any empty spaces, it is invalid
        if '.' in row[:group]:
            return 0
        # All good now, chop off the group and recurse
        return valid_combinations(row[group + 1:], groups[1:])
    # Must have been a '?', which could be '.' or '#', so return the sum
    # of both.
    dot_case = valid_combinations(f'.{rest}', groups)
    octothorpe_case = valid_combinations(f'#{rest}', groups)
    return dot_case + octothorpe_case

def solve(lines: str):
    puzzles = [Puzzle.from_string(line) for line in lines.splitlines()]
    all_results = []
    for puzzle in puzzles:
        all_results.append(valid_combinations(puzzle.row, puzzle.groups))
    print(f'{sum(all_results)}')
    return


if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
