import dataclasses
import numpy as np

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

EMPTY = 0
ROUND = 1
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
            a[line_no] = np.where(arr_line == 'O', ROUND, 0)
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

def solve(lines: str):
    puzzle = Puzzle.from_str(lines)
    puzzle.tilt()
    print(puzzle.score())
    return


if __name__ == '__main__':
    solve(example)
    solve(open('input.txt').read())
