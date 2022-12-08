# Notes:
# Grid of trees, each number is the height of the tree
# Considering only rows and columns (left/right/up/down)
# How many can you see from the outside?

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


def mark_visible(grid):
    visible_grid = np.zeros_like(grid)
    rows, columns = grid.shape
    # Mark trees until highest is found
    for column in range(columns):
        # From top
        row = 0
        tallest = grid[row, column]
        visible_grid[row, column] = 1
        for row in range(1, rows):
            if grid[row, column] > tallest:
                tallest = grid[row, column]
                visible_grid[row, column] = 1
        # From bottom
        row = -1
        tallest = grid[row, column]
        visible_grid[row, column] = 1
        for row in range(1, rows):
            row = -row - 1
            if grid[row, column] > tallest:
                tallest = grid[row, column]
                visible_grid[row, column] = 1
    for row in range(rows):
        # From left
        column = 0
        tallest = grid[row, column]
        visible_grid[row, column] = 1
        for column in range(1, columns):
            if grid[row, column] > tallest:
                tallest = grid[row, column]
                visible_grid[row, column] = 1
        # From right
        column = -1
        tallest = grid[row, column]
        visible_grid[row, column] = 1
        for column in range(1, columns):
            column = -column - 1
            if grid[row, column] > tallest:
                tallest = grid[row, column]
                visible_grid[row, column] = 1
    return visible_grid


grid = parse_grid(test_input)
visible_grid = mark_visible(grid)
print(f'{sum(sum(visible_grid))=}')

grid = parse_grid(open('day8-input.txt').read())
visible_grid = mark_visible(grid)
print(f'{sum(sum(visible_grid))=}')

