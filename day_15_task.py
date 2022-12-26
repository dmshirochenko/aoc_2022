# https://adventofcode.com/2022/day/15

import re
from math import inf

REG_EXP = "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
ROW_TO_CHECK = 2_000_000


def size_map(map_grid, distance_dct):
    c_min = inf
    c_max = -inf
    for point in map_grid.keys():
        sensor_radius = distance_dct.get(point)
        x, y = point
        if sensor_radius:
            c_min = min(x - sensor_radius, c_min)
            c_max = max(x + sensor_radius, c_max)

        c_min = min(x, c_min)
        c_max = max(x, c_max)

    return c_min, c_max


def distance_check(map_grid, distance_dct):
    non_possible_pos = set()
    y = ROW_TO_CHECK
    # for y in range(H_MIN, H_MAX + 1):
    for point_to_check in distance_dct:
        print("point_to_check", point_to_check)
        point_to_check_x, point_to_check_y = point_to_check
        height_diff = abs(y - point_to_check_y)
        if distance_dct[point_to_check] >= height_diff:
            for x in range(C_MIN, C_MAX + 1):
                value_in_the_map_grid = map_grid.get((x, y))
                if value_in_the_map_grid == "#" or value_in_the_map_grid == "B" or value_in_the_map_grid == "S":
                    continue
                elif manhattan_distance((x, y), point_to_check) <= distance_dct[point_to_check]:
                    if y == ROW_TO_CHECK:
                        non_possible_pos.add((x, y))
                    map_grid[(x, y)] = "#"

    return non_possible_pos


def check_the_ranges(distance_dct, y):
    ranges_list = []
    for point_to_check in distance_dct:
        point_to_check_x, point_to_check_y = point_to_check
        height_diff = abs(y - point_to_check_y)
        if height_diff > distance_dct[point_to_check]:
            continue
        col_range = distance_dct[point_to_check] - height_diff
        ranges_list.append((point_to_check_x - col_range, point_to_check_x + col_range))

    ranges_list.sort()
    # print(ranges_list)
    prev_x2 = ranges_list[0][1]
    for x1, x2 in ranges_list[1:]:
        if x1 > prev_x2:
            return prev_x2 + 1
        prev_x2 = max(x2, prev_x2)
    return False


def part_two(distance_dct):
    for y in range(H_MIN, H_MAX + 1):
        if x := check_the_ranges(distance_dct, y):
            return x * 4_000_000 + y


def createTunnels(dct):
    for y in range(H_MIN, H_MAX + 1):
        for x in range(C_MIN, C_MAX + 1):
            print(dct[(x, y)] if (x, y) in dct else ".", sep="", end="")
        print()


def dist_beacon(map_grid):
    for y in range(H_MIN, H_MAX + 1):
        for x in range(C_MIN, C_MAX + 1):
            value_in_the_map_grid = map_grid.get((x, y))
            if value_in_the_map_grid == "#" or value_in_the_map_grid == "B" or value_in_the_map_grid == "S":
                continue
            else:
                return (x, y)


def manhattan_distance(point1, point2):
    distance = 0
    for x1, x2 in zip(point1, point2):
        difference = x2 - x1
        absolute_difference = abs(difference)
        distance += absolute_difference

    return distance


if __name__ == "__main__":
    sensors_list = []
    map_grid = dict()
    distance_dct = dict()
    with open("day_15.txt", "r") as f:
        sensors_list = [re.match(REG_EXP, l.rstrip()) for l in f.readlines()]

    for mathch in sensors_list:
        seansor_coord_x, seansor_coord_y = mathch.group(1, 2)
        map_grid[(int(seansor_coord_x), int(seansor_coord_y))] = "S"
        beacon_coord_x, beacon_coord_y = mathch.group(3, 4)
        map_grid[(int(beacon_coord_x), int(beacon_coord_y))] = "B"
        distance = manhattan_distance(
            (int(seansor_coord_x), int(seansor_coord_y)), (int(beacon_coord_x), int(beacon_coord_y))
        )
        distance_dct[(int(seansor_coord_x), int(seansor_coord_y))] = distance

    # part one
    """
    C_MIN, C_MAX = size_map(map_grid, distance_dct)
    H_MIN = 0
    H_MAX = ROW_TO_CHECK
    non_possible_pos = distance_check(map_grid, distance_dct)
    print("Part one : non_possible_spots", len(non_possible_pos))
    """

    # part two
    C_MIN = 0
    C_MAX = 4_000_000
    H_MIN = 0
    H_MAX = 4_000_000
    print("check_the_ranges", part_two(distance_dct))

    # createTunnels(map_grid)
    # print("dist_beacon ", dist_beacon(map_grid))
