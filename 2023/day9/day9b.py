import numpy as np


# Extrapolate backward this time
# Swap stuff around, use - instead of +

example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

def parse(s: str):
    return np.array([int(v) for v in s.split(' ')])

def find_change(arr: np.ndarray) -> np.ndarray:
    return arr[1:] - arr[:-1]

def project(base: np.ndarray, change: np.ndarray) -> np.ndarray:
    return np.concatenate(
        (np.array([change[0] - base[0]]), change)
    )


def solve_single(single: np.ndarray) -> int:
    arr = single
    changes = [single]
    change = find_change(arr)
    while not np.all(change == 0):
        changes.append(change)
        change = find_change(change)
    changes.append(change)
    changes[-1] = np.concatenate((np.array([0]), changes[-1]))
    tower = [changes.pop()]
    while changes:
        projected = project(tower[-1], changes.pop())
        tower.append(projected)
    return tower[-1][0]

def solve(s: str):
    parsed = [parse(line) for line in s.splitlines()]
    values = [solve_single(p) for p in parsed]
    print(sum(values))
    return

if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
