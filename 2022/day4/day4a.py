# Notes:
# Pairs of elves are cleaning
# Ids are specified from start to end
# Which ones fully overlap?

import numpy as np

test_data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""


def parse_range(range_str):
    start_str, end_str = range_str.split('-')
    return np.arange(int(start_str), int(end_str) + 1)


def fully_overlaps(r_1, r_2):
    intersection = np.intersect1d(r_1, r_2)
    print(f'{intersection=}, {r_1=}, {r_2=}')
    return np.array_equal(intersection, r_1) or np.array_equal(intersection, r_2)


overlap_count = 0
for line in test_data.splitlines(keepends=False):
    elf_1, elf_2 = line.split(',')
    if fully_overlaps(parse_range(elf_1), parse_range(elf_2)):
        overlap_count += 1
print(f'{overlap_count=}')


overlap_count = 0
for line in open('day4-input.txt').readlines():
    elf_1, elf_2 = line.split(',')
    if fully_overlaps(parse_range(elf_1), parse_range(elf_2)):
        overlap_count += 1
print(f'{overlap_count=}')
