'''
It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
'''

from collections import namedtuple
from typing import List
import copy


ExpectedResult = namedtuple('ExpectedResult', 'input output')

inputAList = [246540, 787419]
testAList = [
    ExpectedResult("""111111""", True),
    ExpectedResult("""223450""", False),
    ExpectedResult("""123789""", False),
]


def twoAdjascentStrict(lst: List, joined: str):
    """Returns True if there is a pair present that is not part of a larger group"""
    found = False
    for item in lst:
        if str(item) * 2 in joined and str(item) * 3 not in joined and str(item) * 4 not in joined and str(item) * 5 not in joined and str(item) * 6 not in joined:
            found = True
            break
    return found


def twoAdjascent(lst: List, joined: str):
    found = False
    for item in lst:
        if str(item) * 2 in joined:
            found = True
            break
    return found


def decreases(lst: List):
    sortedList = copy.copy(lst)
    sortedList.sort()
    return lst == sortedList


def validPassword(inp: str, strict=False):
    """Test that the given string is a valid password"""
    valid = True
    splitInts = [int(c) for c in inp]
    if strict:
        valid &= twoAdjascentStrict(splitInts, inp)
    else:
        valid &= twoAdjascent(splitInts, inp)
    valid &= decreases(splitInts)
    return valid


def functionA(start, end):
    """Find the number of valid passwords in the given range"""
    total = 0
    for possible in range(start, end+1):
        if validPassword(str(possible)):
            total += 1
    return total


for inp, outp in testAList:
    ret = validPassword(inp)
    assert ret == outp, '{} != {} for input={}'.format(ret, outp, inp)


print('result A:', functionA(*inputAList))


def functionB(start, end):
    """Find the number of valid passwords in the given range"""
    total = 0
    for possible in range(start, end+1):
        if validPassword(str(possible), strict=True):
            total += 1
    return total


print('result B:', functionB(*inputAList))
