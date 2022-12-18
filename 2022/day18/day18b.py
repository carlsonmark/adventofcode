# Notes
# Aha, I knew it would require checking the interior as well...
# Get the exterior surface area only, but how?
# A naive approach would be to start with all 2s, fill 1s for volume,
# then draw lines from all sides to the half-way point and fill those in with "0".
# Then when counting surfaces, only consider it to be a surface if the neighbour is a 0.
# This would not work for caves where one side is open, but it does not look like that is in this dataset
# Even better, after setting all outside points to 0, change the inside points to 1 to fill in any gaps
# Just don't consider them droplets
# Dang, there are a couple of caves/tunnels, but only 1px deep


import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
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


def visit_voxel(volume, coord):
    keep_visiting = False
    num_neighbours = 2
    if volume[coord] != 1:
        keep_visiting = True
        volume[coord] = 0
        x, y, z = coord
        for x_inc in range(num_neighbours):
            x_inc += 1
            try:
                if volume[x + x_inc, y, z] == 2:
                    volume[x + x_inc, y, z] = 0
                else:
                    break
            except IndexError: pass
        for x_inc in range(num_neighbours):
            x_inc += 1
            try:
                if volume[x - x_inc, y, z] == 2:
                    volume[x - x_inc, y, z] = 0
                else:
                    break
            except IndexError: pass
        for y_inc in range(num_neighbours):
            y_inc += 1
            try:
                if volume[x, y + y_inc, z] == 2:
                    volume[x, y + y_inc, z] = 0
                else:
                    break
            except IndexError: pass
        for y_inc in range(num_neighbours):
            y_inc += 1
            try:
                if volume[x, y - y_inc, z] == 2:
                    volume[x, y - y_inc, z] = 0
                else:
                    break
            except IndexError: pass
        for z_inc in range(num_neighbours):
            z_inc += 1
            try:
                if volume[x, y, z + z_inc] == 2:
                    volume[x, y, z + z_inc] = 0
                else:
                    break
            except IndexError: pass
        for z_inc in range(num_neighbours):
            z_inc += 1
            try:
                if volume[x, y, z - z_inc] == 2:
                    volume[x, y, z - z_inc] = 0
                else:
                    break
            except IndexError: pass

    return keep_visiting


def create_volume(coords):
    max_x = max(coords[:, 0])
    max_y = max(coords[:, 1])
    max_z = max(coords[:, 2])
    volume = np.ones((max_x + 2, max_y + 2, max_z + 2), dtype=int) * 2
    volume[tuple(coords.T)] = 1
    xw, yw, zw = volume.shape
    for x in range(xw):
        for y in range(yw):
            for z in range(zw):
                if not visit_voxel(volume, (x, y, z)):
                    break
            for z in range(zw):
                if not visit_voxel(volume, (x, y, zw-z-1)):
                    break

    for y in range(yw):
        for z in range(zw):
            for x in range(xw):
                if not visit_voxel(volume, (x, y, z)):
                    break
            for x in range(xw):
                if not visit_voxel(volume, (xw-x-1, y, z)):
                    break

    for z in range(zw):
        for x in range(xw):
            for y in range(yw):
                if not visit_voxel(volume, (x, y, z)):
                    break
            for y in range(yw):
                if not visit_voxel(volume, (x, yw-y-1, z)):
                    break
    volume = np.where(volume < 2, volume, 1)
    return volume


def count_outer_surface_single(volume, coord):
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
        count += count_outer_surface_single(volume, coord)
    return count


coords = parse_input(test_input)
volume_ = create_volume(coords)
count_ = count_surface(volume_, coords)
print(f'{count_=}')

coords = parse_input(open('day18-input.txt').read())
volume_ = create_volume(coords)
count_ = count_surface(volume_, coords)
print(f'{count_=}')  # Too low: 2527

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.voxels(volume_, edgecolor='k')
plt.show()


fig = plt.figure()
grid = ImageGrid(fig, 111, nrows_ncols=(5,5))

for i, ax_sl in enumerate(zip(grid, volume_)):
    ax, sl = ax_sl
    ax.imshow(sl, vmin=0, vmax=2)
plt.show()
