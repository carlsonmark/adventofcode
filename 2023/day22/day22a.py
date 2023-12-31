import dataclasses
from copy import deepcopy
from typing import List, Tuple

import numpy as np

example = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

@dataclasses.dataclass
class Cube:
    z: int
    y: int
    x: int
    def to_coords(self):
        return self.z, self.y, self.x


@dataclasses.dataclass
class Brick:
    number: int
    cubes: List[Cube]
    def __lt__(self, other):
        return self.lowest_z() < other.lowest_z()

    def lowest_z(self):
        lowest = 99999999
        for cube in self.cubes:
            lowest = min(lowest, cube.z)
        return lowest

    def drop(self, amount: int=1):
        self.cubes = self.dropped_location(amount)
        return

    def dropped_location(self, amount: int=1) -> List[Cube]:
        cpy = deepcopy(self.cubes)
        for cube in cpy:
            cube.z -= amount
        return cpy

def parse(lines: str) -> Tuple[List[Brick], np.ndarray]:
    bricks = []
    max_x = 0
    max_y = 0
    min_z = 99999999
    max_z = 0
    for count, line in enumerate(lines.splitlines()):
        start, end = line.split('~')
        sx, sy, sz = [int(i) for i in start.split(',')]
        ex, ey, ez = [int(i) for i in end.split(',')]
        cubes = []
        start_x = min(sx, ex)
        end_x = max(sx, ex)
        start_y = min(sy, ey)
        end_y = max(sy, ey)
        start_z = min(sz, ez)
        end_z = max(sz, ez)
        for x in range(end_x-start_x+1):
            for y in range(end_y-start_y+1):
                for z in range(end_z-start_z+1):
                    cz = z+start_z
                    cy = y+start_y
                    cx = x+start_x
                    cubes.append(Cube(z+start_z, y+start_y, x+start_x))
                    max_z = max(cz, max_z)
                    min_z = int(min(cz, min_z))
                    max_y = max(cy, max_y)
                    max_x = max(cx, max_x)
        bricks.append(Brick(count+1, cubes))
    puzzle = np.zeros((max_z+1, max_y+1, max_x+1), dtype=int)
    return bricks, puzzle

def populate_puzzle(bricks, puzzle):
    for brick in bricks:
        for cube in brick.cubes:
            puzzle[cube.to_coords()] = brick.number
    return puzzle

def settle_bricks(bricks, puzzle):
    puzzle = np.zeros_like(puzzle)
    all_settled = True
    for brick in sorted(bricks):
        settled = False
        dropped = brick.dropped_location()
        for cube in dropped:
            # Note: z==0 is the "ground"
            if cube.z < 1:
                settled = True
                break
            else:
                if puzzle[cube.to_coords()] != 0:
                    settled = True
                    break
        if not settled:
            # print('dropping', brick)
            brick.drop(1)
        for cube in brick.cubes:
            puzzle[cube.to_coords()] = brick.number
        if not settled:
            all_settled = False
    return all_settled, puzzle

def show_puzzle(puzzle):
    # Local imports so I can use pypy when not debugging
    import matplotlib.pyplot as plt
    import matplotlib
    import matplotlib.cm as cmx
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(puzzle>0)
    ax.set_aspect('equal')
    plt.show()
    return

def show_slices(puzzle):
    slices = []
    for i in range(puzzle.shape[-1]):
        slices.append(str(puzzle[:, :, i][::-1]).splitlines())
    to_print = ''
    for i in range(len(slices[0])):
        combined = ''
        line_length = len(slices[0][0]) + 5
        for slice in slices:
            combined += f'{slice[i]:{line_length}}'
        to_print += combined + '\n'
    print(to_print)
    return

def solve(lines: str):
    bricks, puzzle = parse(lines)
    all_settled = False
    # populated = populate_puzzle(bricks, np.zeros_like(puzzle))
    # show_puzzle(populated)
    while not all_settled:
        all_settled, puzzle = settle_bricks(bricks, puzzle)
        # for brick in bricks:
        #     print(brick)
        # show_puzzle(puzzle)
    # OK, everything is settled now, see if any bricks can be removed
    show_slices(puzzle)
    # show_puzzle(puzzle)
    can_remove_count = 0
    for brick in bricks:
        bricks_copy = deepcopy(bricks)
        bricks_copy.remove(brick)
        all_settled, puzzle = settle_bricks(bricks_copy, puzzle)
        if all_settled:
            can_remove_count += 1
        print(f'removed {brick}, {all_settled=}')
        # show_slices(puzzle)
    print(can_remove_count)
    return


if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
