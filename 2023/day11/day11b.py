# Expand empty rows and columns by 1000000
# Same as the first part otherwise
from itertools import combinations

import numpy as np


example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

def parse(lines: str):
    splitlines = lines.splitlines()
    galaxy = np.zeros((len(splitlines), len(splitlines[0])), dtype=int)
    for y, line in enumerate(splitlines):
        for x, c in enumerate(line):
            if c == '#':
                galaxy[y, x] = 1
    distances = np.ones_like(galaxy)
    # Get the empty rows and columns
    empty_rows = [
        row_num for row_num in range(galaxy.shape[0]) if (galaxy[row_num, :]==0).all()
    ]
    empty_columns = [
        col_num for col_num in range(galaxy.shape[0]) if (galaxy[:, col_num] == 0).all()
    ]
    for row_num in empty_rows:
        distances[row_num, :] = 1_000_000
    for col_num in empty_columns:
        distances[:, col_num] = 1_000_000
    return galaxy, distances

def calc_distance(star_a: np.ndarray, star_b: np.ndarray, distances: np.ndarray):
    # distance = abs(star_a[0] - star_b[0]) + abs(star_a[1] - star_b[1])
    start_end_rows = tuple(sorted((star_a[0], star_b[0])))
    start_end_cols = tuple(sorted((star_a[1], star_b[1])))
    a_y, a_x = star_a
    b_y, b_x = star_b

    cols_walked = distances[slice(*start_end_rows), start_end_cols[1]]
    rows_walked = distances[start_end_rows[0], slice(*start_end_cols)]
    distance = sum(cols_walked) + sum(rows_walked)
    # print(f'{distance=} for {star_a} to {star_b}, {rows_walked=}, {cols_walked=}, {start_end_cols=}, {start_end_rows=}')
    return distance

def solve(lines: str):
    galaxy, distances = parse(lines)
    np.set_printoptions(threshold=1024)
    print(galaxy)
    print(distances)
    # Get the indexes of each star
    star_positions = np.transpose(np.nonzero(galaxy))
    total_distance = 0
    pairs = combinations(star_positions, 2)
    for star_a, star_b in pairs:
        total_distance += calc_distance(star_a, star_b, distances)
    print(f'{total_distance=}')
    return


if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
