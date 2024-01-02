import dataclasses
from itertools import combinations
from typing import Tuple
import sympy

import numpy as np
from numpy.linalg import LinAlgError

# Hit all hailstones with one carefully thrown rock from an arbitrary
# position and with arbitrary velocity.

"""
Again, from https://www.youtube.com/watch?v=guOyA7Ijqgk
Use sympy... because my brain hurts from too much math...
t = (xr - xh) / (vxh - vxr) = (yr - yh) / (vyh - vyr) = (zr - zh) / (vzh - vzr)
0 = (xr - xh) * (vy - vyr) - (yr - yh) * (vx - vxr)
0 = (yr - yh) * (vz - vzr) - (zr - zh) * (vy - vyr)
"""

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

    def position(self) -> Tuple[int, int, int]:
        return self.px, self.py, self.pz

    def velocity(self) -> Tuple[int, int, int]:
        return self.vx, self.vy, self.vz


def intersection(h1: Hailstone, h2: Hailstone):
    a1, b1, c1 = h1.to_standard_form()
    a2, b2, c2 = h2.to_standard_form()
    return np.linalg.solve([[a1, b1], [a2, b2]], [c1, c2])

def parse(lines: str):
    hailstones = [Hailstone.from_str(line) for line in lines.splitlines()]
    return hailstones

def solve(lines: str):
    hailstones = parse(lines)
    xr, yr, zr, vxr, vyr, vzr = sympy.symbols('xr, yr, zr, vxr, vyr, vzr')
    equations = []
    for hailstone in hailstones[:6]:
        px, py, pz = hailstone.position()
        vx, vy, vz = hailstone.velocity()
        equations.append((xr - px) * (vy - vyr) - (yr - py) * (vx - vxr))
        equations.append((yr - py) * (vz - vzr) - (zr - pz) * (vy - vyr))
    solutions = sympy.solve(equations)
    if len(solutions) != 1:
        print(f'Use more data, {solutions=}')
        return
    solution = solutions[0]
    xr = solution[xr]
    yr = solution[yr]
    zr = solution[zr]
    print(f'{xr + yr + zr=}')
    return


if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
