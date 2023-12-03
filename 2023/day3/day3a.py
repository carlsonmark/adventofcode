from typing import List

# Find numbers that are touching a non-number symbol (excluding '.')
# Add those up

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


def is_part_number(lines:List[str], position: int, special_chars: str) -> bool:
    is_pn = False
    if position == 0:
        # first character in the line
        is_pn |= lines[0][position] in special_chars
        is_pn |= lines[2][position] in special_chars
        is_pn |= lines[0][position+1] in special_chars
        is_pn |= lines[1][position+1] in special_chars
        is_pn |= lines[2][position+1] in special_chars
    elif position == len(lines[0]) - 1:
        # last character in the line
        is_pn |= lines[0][position-1] in special_chars
        is_pn |= lines[1][position-1] in special_chars
        is_pn |= lines[2][position-1] in special_chars
        is_pn |= lines[0][position] in special_chars
        is_pn |= lines[2][position] in special_chars
    else:
        # middle of the line
        is_pn |= lines[0][position - 1] in special_chars
        is_pn |= lines[1][position - 1] in special_chars
        is_pn |= lines[2][position - 1] in special_chars
        is_pn |= lines[0][position] in special_chars
        is_pn |= lines[2][position] in special_chars
        is_pn |= lines[0][position + 1] in special_chars
        is_pn |= lines[1][position + 1] in special_chars
        is_pn |= lines[2][position + 1] in special_chars
    return is_pn


def strip_all_numbers(lines: str):
    reduced = ''.join(set(lines))
    for c in '0123456789.\n':
        reduced = reduced.replace(c, '')
    return reduced


def find_all_part_numbers(lines: List[str], special_chars: str) -> List[int]:
    part_numbers = []
    for line_number, line in enumerate(lines[1:-1]):
        pn_str = ''
        is_pn = False
        for i, c in enumerate(line):
            if c in '0123456789':
                # Check if this is a part number
                is_pn |= is_part_number([lines[line_number], lines[line_number + 1], lines[line_number + 2]], i, special_chars)
                # Append to the part number string
                pn_str += c
            elif pn_str:
                # Done
                if is_pn:
                    part_numbers.append(int(pn_str))
                pn_str = ''
                is_pn = False
        # Catch any last number in a line:
        if is_pn:
            part_numbers.append(int(pn_str))
    return part_numbers


def solve(lines: str):
    # pad lines first so all can be parsed the same way
    special_chars = strip_all_numbers(lines)
    lines = lines.splitlines()
    lines.insert(0, '.' * len(lines[1]))
    lines.append('.' * len(lines[1]))
    part_numbers = find_all_part_numbers(lines, special_chars)
    for pn in part_numbers:
        print(pn)
    print(f'{sum(part_numbers)=}')
    return


if __name__ == '__main__':
    solve(example)
    solve(open('day3input.txt').read())
    # 536884, too low
