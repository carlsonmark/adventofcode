# Notes:
# Signal coming from an unknown beacon
# x and y coords for the beacon must be between 0 and 4000000 (0 to 20 for test data)
# Tuning frequency calculation is x * 4000000 + y
# Find the only position in the search area that could have a beacon, what is its tuning frequency?

import re

test_input = """\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""


def parse_sensors_and_beacons(s):
    sensors_beacons = []
    for line in s.splitlines(keepends=False):
        s_x, s_y, b_x, b_y = [int(_) for _ in re.findall(r'-?\d+', line)]
        sensors_beacons.append(((s_x, s_y), (b_x, b_y)))
    return sensors_beacons


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def compute_distances(sensors_beacons):
    sensors_distances = []
    for sensor, beacon in sensors_beacons:
        distance = manhattan_distance(sensor, beacon)
        sensors_distances.append((sensor, distance))
    return sensors_distances


def find_intersections(sensor, distance, line_y):
    x, y = sensor
    dy = abs(line_y - y)
    if dy >= distance:
        # Does not overlap
        return None
    # Overlaps
    extra_y = distance - abs(line_y - y)
    half_width = extra_y
    return x - half_width, x + half_width


def merge_intersections(intersections):
    found_intersections = []
    sorted_intersections = list(reversed(sorted(intersections)))
    start, end = sorted_intersections.pop()
    while sorted_intersections:
        intersection = sorted_intersections.pop()
        if intersection[0] <= (end + 1):
            # Next start lines up with the end, extending.
            # Keep in mind that the previous end might be larger!
            end = max(end, intersection[1])
        else:
            # Gap
            found_intersections.append((start, end))
            start, end = intersection
    found_intersections.append((start, end))
    return found_intersections


s_b = parse_sensors_and_beacons(test_input)
s_d = compute_distances(s_b)
for y in range(0, 21):
    intersections = []
    for s, d in s_d:
        sensor_intersection = find_intersections(s, d, y)
        if sensor_intersection is not None:
            intersections.append(sensor_intersection)
    print(f'{y=}, {sorted(intersections)=}')
    merged = merge_intersections(intersections)
    print(f'{y=}, {merged=}')


# s_b = parse_sensors_and_beacons(open('day15-input.txt').read())
# s_d = compute_distances(s_b)
# for y in range(0, 4000000):
#     intersections = []
#     for s, d in s_d:
#         sensor_intersection = find_intersections(s, d, y)
#         if sensor_intersection is not None:
#             intersections.append(sensor_intersection)
#     merged = merge_intersections(intersections)
#     if len(merged) > 1:
#         print(f'{y=}, {merged=}')

# The above printed:
# y=3267339, merged=[(-337846, 2557296), (2557298, 4214118)]
# So:
y = 3267339
x = 2557297
tuning_frequency = x * 4000000 + y
print(f'{tuning_frequency=}')
