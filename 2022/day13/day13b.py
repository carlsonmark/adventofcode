# Notes
# Compare as before... but sort all packets using this comparison
# Exclude blank lines
# Find [[2]] and [[6]] and multiply their indexes (1 based)

import ast
from functools import cmp_to_key

test_input = """\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]

"""


def parse_packets(s):
    packets = []
    lines = s.splitlines(keepends=False)
    for line in lines:
        if line:
            packets.append(ast.literal_eval(line))
    packets.append([[2]])
    packets.append([[6]])
    return packets


# If both values are integers, then the lower integer should come first
#


class CorrectOrder(Exception):
    pass


class WrongOrder(Exception):
    pass


def compare_single(l1, l2):
    # If one is an integer and other is a list, convert integer to a list (list of one value)
    if isinstance(l1, list):
        if not isinstance(l2, list):
            l2 = [l2]
    if isinstance(l2, list):
        if not isinstance(l1, list):
            l1 = [l1]
    if isinstance(l1, int) and isinstance(l2, int):
        # - left < right: correct order (done comparing?)
        # - left > right: wrong order (done comparing)
        # - left == right: continue comparing
        if l1 < l2:
            print(f'Correct: {l1} < {l2}')
            raise CorrectOrder()
        if l1 > l2:
            print(f'Wrong: {l1} > {l2}')
            raise WrongOrder()
        if l1 == l2:
            return
    if isinstance(l1, list) and isinstance(l2, list):
        # If both values are list, compare first value from each list, then second value, etc
        i = 0
        while i < len(l1):
            if i == len(l1) and i == len(l2):
                # If lists are same length and comparison says to continue, then continue
                return
            if i == len(l1) and i < len(l2):
                # If left runs out of items first, inputs are in the correct order
                print(f'Correct: {i} {len(l1)=}')
                raise CorrectOrder()
            if i >= len(l2):
                # If right runs out of inputs first, wrong order
                print(f'Wrong: {i} {len(l2)=}')
                raise WrongOrder()
            l = l1[i]
            r = l2[i]
            compare_single(l, r)
            i += 1
        if i == len(l1) and i < len(l2):
            # If left runs out of items first, inputs are in the correct order
            print(f'Correct: {i} {len(l1)=}')
            raise CorrectOrder()


def compare(item1, item2):
    try:
        compare_single(item1, item2)
    except CorrectOrder:
        return -1
    except WrongOrder:
        return 0
    return -1

packets_ = parse_packets(test_input)
sorted_ = list(sorted(packets_, key=cmp_to_key(compare)))
for p in sorted_:
    print(p)
i_2 = sorted_.index([[2]]) + 1
i_6 = sorted_.index([[6]]) + 1
print(f'{i_2 * i_6=}')

packets_ = parse_packets(open('day13-input.txt').read())
sorted_ = list(sorted(packets_, key=cmp_to_key(compare)))
for p in sorted_:
    print(p)
i_2 = sorted_.index([[2]]) + 1
i_6 = sorted_.index([[6]]) + 1
print(f'{i_2 * i_6=}')
