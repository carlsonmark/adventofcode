# Detect mirroring, but with exactly one error
import dataclasses
from typing import List
import numpy as np

example = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

@dataclasses.dataclass
class Map:
    m: np.ndarray

    @classmethod
    def from_str(cls, lines: List[str]):
        m = np.array([list(line) for line in lines])
        return cls(m)

def symm_horiz(a: np.ndarray) -> int:
    return symm_vert(a.transpose())

def symm_vert(a: np.ndarray) -> int:
    num_rows = a.shape[0]
    for row in range(num_rows-1):
        off_by = check_symm_vert(a, row + 1)
        if off_by == 1:
            return row + 1
    return None

def check_symm_vert(a: np.ndarray, pos: int) -> int:
    num_rows = a.shape[0]
    start_row = num_rows / 2
    end_row = num_rows / 2
    if pos > num_rows / 2:
        end_row = num_rows
        start_row = num_rows - (num_rows - pos) * 2
    elif pos < num_rows / 2:
        start_row = 0
        end_row = pos * 2
    first_half = a[start_row:pos]
    flipped_half = np.flip(a[pos:end_row], 0)
    return np.product(first_half.shape) - sum(sum(first_half == flipped_half))

def parse(lines: str) -> List[Map]:
    block = []
    maps = []
    for line in lines.splitlines():
        if line:
            block.append(line)
        else:
            maps.append(Map.from_str(block))
            block = []
    maps.append(Map.from_str(block))
    return maps

def solve(lines: str):
    maps = parse(lines)
    total = 0
    for m in maps:
        h_pos = symm_horiz(m.m)
        if h_pos is not None:
            total += h_pos
        else:
            v_pos = symm_vert(m.m)
            total += 100 * v_pos
    print(total)
    return

if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
