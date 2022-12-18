# Notes
# Find surface area of lava droplets
# 3D coordinates
# Find all exposed sides? Including ones that are inside an enclosed space I guess?

import matplotlib.pyplot as plt
import numpy as np


test_input = """\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""


def parse_input(s):
    num_lines = s.count('\n')
    coords = np.zeros((num_lines, 3), dtype=int)
    for i, line in enumerate(s.splitlines(keepends=False)):
        coords[i] = [int(c) for c in line.split(',')]
    return coords


def create_volume(coords):
    max_x = max(coords[:, 0])
    max_y = max(coords[:, 1])
    max_z = max(coords[:, 2])
    volume = np.zeros((max_x + 2, max_y + 2, max_z + 2), dtype=int)
    volume[tuple(coords.T)] = 1
    return volume


def count_surface_single(volume, coord):
    above = coord[0], coord[1] + 1, coord[2]
    below = coord[0], coord[1] - 1, coord[2]
    left = coord[0] + 1, coord[1], coord[2]
    right = coord[0] - 1, coord[1], coord[2]
    front = coord[0], coord[1], coord[2] + 1
    back = coord[0], coord[1], coord[2] - 1
    count = 6
    for relative_coord in (above, below, left, right, front, back):
        count -= volume[relative_coord]
    return count


def count_surface(volume, coords):
    count = 0
    for coord in coords:
        count += count_surface_single(volume, coord)
    return count


coords = parse_input(test_input)
volume_ = create_volume(coords)
count_ = count_surface(volume_, coords)
print(f'{count_=}')

coords = parse_input(open('day18-input.txt').read())
volume_ = create_volume(coords)
count_ = count_surface(volume_, coords)
print(f'{count_=}')

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.voxels(volume_, edgecolor='k')
plt.show()
