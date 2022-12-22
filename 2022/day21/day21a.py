# Notes
# monkey name: operation
# Eval them all until "root" is a number?

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


d_ = parse_input(test_input)
while isinstance(d_['root'], str):
    d_ = eval_all(d_)
print(d_['root'])

d_ = parse_input(open('day21-input.txt').read())
while isinstance(d_['root'], str):
    d_ = eval_all(d_)
print(d_['root'])
