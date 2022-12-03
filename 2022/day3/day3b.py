# Notes:
# Elves have badges, there are 3 per group
# Each set of 3 lines is a group
# Each group can have a different badge type
# Find which item is in all 3 lines

def score_priority(item):
    ord_item = ord(item)
    if ord_item <= ord('Z'):
        return ord_item - ord('A') + 1 + 26
    return ord_item - ord('a') + 1


def find_badge(group):
    first_line = group[0]
    for item in first_line:
        if item in group[1] and item in group[2]:
            return item


def calculate_priority(group):
    badge = find_badge(group)
    return score_priority(badge)


def create_groups(lines):
    groups = []
    group = []
    for line in lines:
        group.append(line)
        if len(group) == 3:
            groups.append(group)
            group = []
    return groups



test_data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

groups = create_groups(test_data.splitlines(keepends=False))
total = 0
for group in groups:
    total += calculate_priority(group)
print(f'Test: {total=}')

total = 0
groups = create_groups(open('day3-input.txt').readlines())
for group in groups:
    total += calculate_priority(group)
print(f'{total=}')
