# Notes:
# Find the start of packet marker
# Start is 4 bytes after finding non-repeating characters


test_data = {
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 7,
    "bvwbjplbgvbhsrlpgdmjqwftvncz": 5,
    "nppdvjthqldpwncqszvftbrmjlhg": 6,
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 10,
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 11,
}


def find_start(data):
    start = 0
    while len(set(data[start:start+4])) != 4:
        start += 1
    return start + 4


for d, expected in test_data.items():
    print(f'{find_start(d)=}, {expected=}')


print(find_start(open('day6-input.txt').read()))
