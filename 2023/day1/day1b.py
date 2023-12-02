import re

example = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""
calibration_values=[29, 83, 13, 24, 42, 14, 76]
test_total=281

# Get first and last digit from each line to make a two digit number, then sum them

replacements = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

def pre_filter_line(line: str) -> str:
    i = 0
    filtered = ''
    while i < len(line):
        replaced = False
        for k in replacements:
            if line[i:i+len(k)] == k:
                filtered += replacements[k]
                replaced = True
                break
        if not replaced:
            filtered += line[i]
        # Always increment by one, no matter how many letters were matched
        i += 1
    return filtered

def filter_line(line: str) -> str:
    matches = re.findall(r'\d', pre_filter_line(line))
    filtered = ''.join(matches)
    return filtered
def solution(input: str):
    values = []
    for line in input.splitlines():
        numbers = filter_line(line)
        first = numbers[0]
        last = numbers[-1]
        values.append(int(first + last))
    print(f'{values=}')
    return sum(values)

if __name__ == '__main__':
    print([pre_filter_line(line) for line in example.splitlines()])
    print(solution(example))
    print(solution(open('day1input.txt').read()))

# 53551 too high
