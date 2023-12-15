import dataclasses
import time

import numpy as np

# Yay for numpy rotation
# Boo for off by one based questions and zero based array indexes

example = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

EMPTY = 1
ROUND = 0
CUBE = 2

@dataclasses.dataclass
class Puzzle:
    a: np.ndarray
    @classmethod
    def from_str(self, lines: str):
        lines = lines.splitlines()
        a = np.zeros((len(lines), len(lines[0])), dtype=int)
        for line_no, line in enumerate(lines):
            arr_line = np.array(list(line))
            a[line_no] = np.where(arr_line == 'O', ROUND, EMPTY)
            a[line_no] = np.where(arr_line == '#', CUBE, a[line_no])
        return Puzzle(a)

    def score(self) -> int:
        # Flip so row+1 is the row number for the score
        flipped = np.flip(self.a, 0)
        score = 0
        for i, row in enumerate(flipped):
            score += sum(row==ROUND) * (i+1)
        return score

    def tilt(self):
        still_rolling = True
        while still_rolling:
            still_rolling = False
            for i, row in enumerate(self.a):
                # Skip the first row
                if i == 0:
                    continue
                for j, boulder in enumerate(row):
                    if self.a[i, j] == ROUND and self.a[i - 1, j] == EMPTY:
                        self.a[i - 1, j] = ROUND
                        self.a[i, j] = EMPTY
                        still_rolling = True
        return

    def rot90(self):
        self.a = np.rot90(self.a, -1)
        return

def solve(lines: str):
    puzzle = Puzzle.from_str(lines)
    scores = []
    rep_check_length = 20
    cycles = 0
    while True:
        tStart = time.monotonic()
        puzzle.tilt()
        puzzle.rot90()
        puzzle.tilt()
        puzzle.rot90()
        puzzle.tilt()
        puzzle.rot90()
        puzzle.tilt()
        puzzle.rot90()
        scores.append(puzzle.score())
        print(cycles, time.monotonic() - tStart)
        # Detect repetition
        if cycles > (2*rep_check_length)+1:
            first_rep = None
            for i in range(len(scores)):
                if i == 0:
                    continue
                check_start = cycles - rep_check_length * 2
                if scores[check_start:check_start+rep_check_length] == scores[check_start+i:check_start+rep_check_length+i]:
                    if first_rep is None:
                        first_rep = i
                    else:
                        rep_rate = i - first_rep
                        remainder = (1000000000 % rep_rate)
                        score_at = check_start
                        while score_at % rep_rate != 0:
                            score_at -= 1
                        score_at += rep_rate * 2 + remainder
                        # Subtract one because the array index is 0 base and
                        # cycle count is 1 based.
                        score_at -= 1
                        score = scores[score_at]
                        print(f'scores[{score_at}]={score}')
                        return
        cycles += 1
    return

if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
