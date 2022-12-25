# Notes
# Base conversion, base 5 with "=" meaning 3 and "-" meaning 4

import numpy as np

test_input = """\
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""


def convert_base(s: str):
    b = 5
    converted = 0
    l = list(s)
    while True:
        try:
            c = l.pop()
            if c == '=':
                n = -2
            elif c == '-':
                n = -1
            else:
                n = int(c)
            converted += n * (b / 5)
            b *= 5
        except IndexError:
            break
    return converted


def parse_input(s: str):
    lst = [convert_base(l) for l in s.splitlines(keepends=False)]
    return lst


def convert_back(val: int):
    base_5 = np.base_repr(int(val), 5)
    inc = 0
    s = ''
    for c in reversed(base_5):
        n = int(c) + inc
        if n == 3:
            converted = '='
            inc = 1
        elif n == 4:
            converted = '-'
            inc = 1
        elif n == 5:
            converted = '0'
            inc = 1
        else:
            converted = str(n)
            inc = 0
        s = converted + s
    if inc:
        s = str(inc) + s
    return s


fuel_ = parse_input(test_input)
print(fuel_)
print(f'{sum(fuel_)=}')

print(convert_back(sum(fuel_)))
print([convert_back(fuel) for fuel in fuel_])

fuel_ = parse_input(open('day25-input.txt').read())
print(convert_back(sum(fuel_)))
# Not: 2---=12=21--=01--000

"""
 SNAFU  Decimal
1=-0-2     1747
 12111      906
  2=0=      198
    21       11
  2=01      201
   111       31
 20012     1257
   112       32
 1=-1=      353
  1-12      107
    12        7
    1=        3
   122       37
"""
