# Find "gear ratios" (product) of numbers that touch a '*' symbol
# Idea: Parse part numbers like before, but keep track of the index of
#       which '*' symbol they touch. At the end, go through the list of
#       '*' symbols and sum the products if there are exactly two for each gear.
from typing import List, Optional, Tuple, Dict

example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
# sum: 4361


def check_gear_pos(lines: List[str], line_no: int, position: int, gear_pos: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    if gear_pos:
        return gear_pos
    try:
        if lines[line_no][position] == '*':
            gear_pos = (line_no, position)
    except IndexError:
        pass
    return gear_pos


search_directions = (
    (0, -1), (0, 0), (0, 1),
    (1, -1),         (1, 1),
    (2, -1), (2, 0), (2, 1)
)


def find_gear_position(lines:List[str], line_number: int, position: int, gear_pos: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    if gear_pos:
        return gear_pos
    for up_down, left_right in search_directions:
        gear_pos = check_gear_pos(lines, line_number + up_down, position + left_right, gear_pos)
    return gear_pos


def find_all_gears(lines: List[str]) -> Dict[Tuple[int, int], List[int]]:
    gears = {}
    for line_number, line in enumerate(lines[1:-1]):
        pn_str = ''
        gear_pos = None
        for i, c in enumerate(line):
            if c in '0123456789':
                # Check if this is next to a gear
                gear_pos = find_gear_position(lines, line_number, i, gear_pos)
                # Append to the part number string
                pn_str += c
            elif gear_pos is not None:
                # Done
                try:
                    gears[gear_pos].append(int(pn_str))
                except KeyError:
                    gears[gear_pos] = [int(pn_str)]
                pn_str = ''
                gear_pos = None
            else:
                pn_str = ''
        # Catch any last number in a line:
        if gear_pos is not None:
            try:
                gears[gear_pos].append(int(pn_str))
            except KeyError:
                gears[gear_pos] = [int(pn_str)]
    return gears


def solve(lines: str):
    # pad lines first so all can be parsed the same way
    lines = lines.splitlines()
    lines.insert(0, '.' * len(lines[1]))
    lines.append('.' * len(lines[1]))
    gears = find_all_gears(lines)
    prod_sum = 0
    for part_numbers in gears.values():
        print(part_numbers)
        if len(part_numbers) == 2:
            prod_sum += part_numbers[0] * part_numbers[1]
    print(f'{prod_sum=}')
    return


if __name__ == '__main__':
    solve(example)
    solve(open('day3input.txt').read())
