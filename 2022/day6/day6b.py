# Notes:
# Find the start of packet marker
# Start is 14 bytes after finding non-repeating characters


test_data = {
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb": 19,
    "bvwbjplbgvbhsrlpgdmjqwftvncz": 23,
    "nppdvjthqldpwncqszvftbrmjlhg": 23,
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg": 29,
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw": 26,
}


def find_start(data):
    start = 0
    while len(set(data[start:start+14])) != 14:
        start += 1
        assert start < len(data)
    return start + 14


for d, expected in test_data.items():
    print(f'{find_start(d)=}, {expected=}')


print(find_start(open('day6-input.txt').read()))
