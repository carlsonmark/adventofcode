# Notes
# Root should be checking that the two numbers match
# humn is me, and I need to brute force the solution to get the numbers to match?
from copy import deepcopy

test_input = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""


def parse_input(s):
    d = {}
    for line in s.splitlines(keepends=False):
        k, v = line.split(': ')
        d[k] = v
    return d


def eval_all(d):
    for k, v in d.items():
        if isinstance(v, str):
            if v.isnumeric():
                d[k] = eval(v)
            else:
                ops = v.split()
                op1 = ops[0]
                op2 = ops[-1]
                if not isinstance(d[op1], str) and not isinstance(d[op2], str):
                    v = eval(v, {}, d)
                    d[k] = v
    return d


# d_ = parse_input(test_input)
# root = d_['root']
# del d_['root']
# root_1 = root.split()[0]
# root_2 = root.split()[-1]
# i = 0
# while True:
#     d_copy = deepcopy(d_)
#     d_copy['humn'] = i
#     while isinstance(d_copy[root_1], str) or isinstance(d_copy[root_2], str):
#         d_copy = eval_all(d_copy)
#     print(f'Tried {i}: {d_copy[root_1]} ?= {d_copy[root_2]}')
#     if d_copy[root_1] == d_copy[root_2]:
#         break
#     i += 1


d_ = parse_input(open('day21-input.txt').read())
root = d_['root']
del d_['root']
root_1 = root.split()[0]
root_2 = root.split()[-1]
i = 3200000000000
inc = 100000000000
dir = 1
while True:
    d_copy = deepcopy(d_)
    d_copy['humn'] = i + inc
    while isinstance(d_copy[root_1], str) or isinstance(d_copy[root_2], str):
        d_copy = eval_all(d_copy)
    diff = d_copy[root_1]-d_copy[root_2]
    print(f'Tried {i + inc}: {d_copy[root_1]} ?= {d_copy[root_2]}: {diff}, {inc}')
    if diff == 0:
        break
    if diff > 0:
        i += inc * dir
        if dir == -1:
            inc /= 10
        dir = 1
    if diff < 0:
        i += inc * dir
        if dir == 1:
            inc /= 10
        dir = -1
