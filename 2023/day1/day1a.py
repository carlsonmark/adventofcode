import re

example = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""
calibration_values=[12, 38, 15, 77]
test_total=142

# Get first and last digit from each line to make a two digit number, then sum them

def filter_line(line: str) -> str:
    matches = re.findall(r'\d', line)
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
    print(solution(example))
    print(solution(open('day1input.txt').read()))
