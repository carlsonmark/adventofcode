import dataclasses
from itertools import combinations
from typing import Tuple

import numpy as np
from numpy.linalg import LinAlgError

example = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

@dataclasses.dataclass
class Hailstone:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int
    @classmethod
    def from_str(cls, line: str):
        pos, vel = line.split(' @ ')
        poss = pos.split(', ')
        vels = vel.split(', ')
        px, py, pz = [int(n) for n in poss]
        vx, vy, vz = [int(n) for n in vels]
        return Hailstone(px, py, pz, vx, vy, vz)

    def to_standard_form(self) -> Tuple[float, float, float]:
        # Convert the position + velocity into standard line form.
        # From https://www.youtube.com/watch?v=guOyA7Ijqgk
        a = self.vy
        b = -self.vx
        c = self.vy * self.px - self.vx * self.py
        return a, b, c

    def intersection_time(self, x: float):
        # Solve for t, from same video above
        return (self.px - x) / self.vx

def intersection(h1: Hailstone, h2: Hailstone):
    a1, b1, c1 = h1.to_standard_form()
    a2, b2, c2 = h2.to_standard_form()
    return np.linalg.solve([[a1, b1], [a2, b2]], [c1, c2])

def parse(lines: str):
    hailstones = [Hailstone.from_str(line) for line in lines.splitlines()]
    return hailstones

def solve(lines: str, min_xy: float, max_xy: float):
    count = 0
    hailstones = parse(lines)
    for (h1, h2) in combinations(hailstones, 2):
        try:
            x, y = intersection(h1, h2)
            t_h1 = h1.intersection_time(x)
            t_h2 = h2.intersection_time(x)
            x_in_range = min_xy <= x <= max_xy
            y_in_range = min_xy <= y <= max_xy
            if x_in_range and y_in_range and t_h1 < 0 and t_h2 < 0:
                count += 1
        except LinAlgError:
            # They do not intersect
            continue
    print(count)
    return


if __name__ == '__main__':
    solve(example, min_xy=7, max_xy=27)
    solve(open('input.txt').read(), min_xy=200000000000000, max_xy=400000000000000)
