# Notes:
# Two compartments per rucksack
# Items go in one of the two
# One wrong item type per rucksack
# Input is items in each rucksack
# Items are identified by a single lowercase or uppercase letter
# One line per rucksack
# First half of the line is the items in the first compartment, second is second

def needs_rearrangement(c_1, c_2):
    for item in c_1:
        for other in c_2:
            if item == other:
                return item


def score_priority(item):
    ord_item = ord(item)
    if ord_item <= ord('Z'):
        return ord_item - ord('A') + 1 + 26
    return ord_item - ord('a') + 1


def calculate_priority(rucksack):
    total_items = len(rucksack)
    compartment_1 = rucksack[:total_items//2]
    compartment_2 = rucksack[total_items//2:]
    priority = needs_rearrangement(compartment_1, compartment_2)
    score = score_priority(priority)
    # print(f'{priority=}, {score=}')
    return score


test_data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

test_results = [16, 38, 42, 22, 20, 19]
test_result = 157

sum_priorities = 0
for line in test_data.splitlines(keepends=False):
    priority = calculate_priority(line)
    sum_priorities += priority

print(f'{sum_priorities=}')

sum_priorities = 0
for line in open('day3-input.txt').readlines():
    priority = calculate_priority(line)
    sum_priorities += priority
print(f'{sum_priorities=}')
