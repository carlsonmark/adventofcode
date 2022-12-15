# Notes
# Compare pairs of packets
# Some are out of order
# Packets contain lists and integers, seems like I can just literal_eval the lines
# When comparing values in the packet the first is the left and the second is the right
# If both values are integers, then the lower integer should come first
# - left < right: correct order (done comparing?)
# - left > right: wrong order (done comparing)
# - left == right: continue comparing
# If both values are list, compare first value from each list, then second value, etc
# - If left runs out of items first, inputs are in the correct order
# - If right runs out of inputs first, wrong order
# - If lists are same length and comparison says to continue, then continue
# If one is an integer and other is a list, convert integer to a list (list of one value)
# then compare
import ast

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


def parse_pairs(s):
    pairs = []
    lines = s.splitlines(keepends=False)
    pair = []
    for line in lines:
        if not line:
            pairs.append(pair)
            pair = []
            continue
        pair.append(ast.literal_eval(line))
    return pairs


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


pairs_ = parse_pairs(test_input)
correct_order = 0
for i, pair in enumerate(pairs_):
    try:
        print(f'Comparing {i+1} {pair[0]} vs {pair[1]}')
        compare_single(pair[0], pair[1])
        correct_order += i + 1
        print(f'Correct')
    except CorrectOrder:
        correct_order += i + 1
        print(f'Correct')
    except WrongOrder:
        pass
print(f'{correct_order=}')


pairs_ = parse_pairs(open('day13-input.txt').read())
correct_order = 0
for i, pair in enumerate(pairs_):
    try:
        print(f'Comparing {i+1} {pair[0]} vs {pair[1]}')
        compare_single(pair[0], pair[1])
        correct_order += i + 1
        print(f'Correct')
    except CorrectOrder:
        correct_order += i + 1
        print(f'Correct')
    except WrongOrder:
        pass
print(f'{correct_order=}')
