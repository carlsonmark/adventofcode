# Notes:
# Beacons and sensors
# A sensor monitors a single beacon
# Sensor only monitors the closest beacon (manhattan distance)
# Considerations:
# Map is probably too big to just fill in and walk
# Even a sparse map would be quite slow
# Plan:
# Compute manhattan distance for each sensor -> beacon pair
# For x values that are near the sensors, see if the manhattan
# distance of each x value is within the manhattan distance.
# If so, add it to a set of x values.

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
        return []
    # Overlaps
    extra_y = distance - abs(line_y - y)
    half_width = extra_y
    return set(range(x - half_width, x + half_width + 1))


s_b = parse_sensors_and_beacons(test_input)
s_d = compute_distances(s_b)
intersections = set()
y = 10
for s, d in s_d:
    sensor_intersection = find_intersections(s, d, y)
    intersections.update(sensor_intersection)
# Remove beacons (and sensors?)
for s, b in s_b:
    if s[1] == y:
        try:
            intersections.remove(s[0])
        except KeyError:
            pass
    if b[1] == y:
        try:
            intersections.remove(b[0])
        except KeyError:
            pass
print(len(intersections))

s_b = parse_sensors_and_beacons(open('day15-input.txt').read())
s_d = compute_distances(s_b)
intersections = set()
y = 2000000
for s, d in s_d:
    sensor_intersection = find_intersections(s, d, y)
    intersections.update(sensor_intersection)
# Remove beacons (and sensors?)
for s, b in s_b:
    if s[1] == y:
        try:
            intersections.remove(s[0])
        except KeyError:
            pass
    if b[1] == y:
        try:
            intersections.remove(b[0])
        except KeyError:
            pass
print(len(intersections))  # 5589545 too high, accidentally used y=10 again!
