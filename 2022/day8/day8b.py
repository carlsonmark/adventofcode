# Notes:
# Elves want to see trees from their treehouse
# Calculate a "scenic score" for each position on the grid
# Scenic score is the multiple of the number of trees in each direction
# The eaves block the view of trees taller than the one that is being considered

import numpy as np

test_input = """30373
25512
65332
33549
35390
"""


def parse_grid(test_input):
    grid = np.zeros((test_input.index('\n'), test_input.count('\n')), dtype=int)
    for row, line in enumerate(test_input.splitlines(keepends=False)):
        for column, tree in enumerate(line):
            grid[row, column] = int(tree)
    return grid


def trees_visible(grid, row, column, row_step=0, column_step=0):
    visible = 0
    base_height = grid[row, column]
    try:
        while True:
            row += row_step
            column += column_step
            if row < 0 or column < 0:
                break
            tree = grid[row, column]
            visible += 1
            if tree >= base_height:
                break
    except IndexError:
        pass
    return visible


def compute_scenic_score(grid, row, column):
    up_score = trees_visible(grid, row, column, row_step=-1)
    down_score = trees_visible(grid, row, column, row_step=1)
    left_score = trees_visible(grid, row, column, column_step=-1)
    right_score = trees_visible(grid, row, column, column_step=1)
    scenic_score = up_score * down_score * left_score * right_score
    return scenic_score


def compute_score_grid(grid):
    score_grid = np.zeros_like(grid)
    rows, cols = grid.shape
    for row in range(rows):
        for col in range(cols):
            score_grid[row, col] = compute_scenic_score(grid, row, col)
    return score_grid


grid = parse_grid(test_input)
score_grid = compute_score_grid(grid)
print(f'{np.max(score_grid)=}')

grid = parse_grid(open('day8-input.txt').read())
score_grid = compute_score_grid(grid)
print(f'{np.max(score_grid)=}')
