from aocd import get_data, submit1, submit2
from days import days

import collections
import re
import string

def day6(submit_answer=False):
    data = get_data(day=6, year=2018).split("\n")

    answer1 = 0
    answer2 = 0

    locations = {}
    total_safe_area = 0

    regex = re.compile(r"(\d+)")

    coords = []

    for coord in data:
        x, y = map(int, regex.findall(coord))
        coords.append((x, y))

    max_x = max(coords, key=lambda x: x[0])[0]
    max_y = max(coords, key=lambda x: x[1])[1]
    min_x = min(coords, key=lambda x: x[0])[0]
    min_y = min(coords, key=lambda x: x[1])[1]

    points_on_edge = set()

    for y in range(min_x, max_y+1):
        for x in range(min_x, max_x+1):
            closest_point = coords[0]
            closest_distance = 10000000000
            equidistance = -1
            sum_distances = 0
            for coord in coords:
                pos_x, pos_y = coord
                distance = abs(pos_x - x) + abs(pos_y - y)
                sum_distances += distance
                if distance < closest_distance:
                    closest_point = coord
                    closest_distance = distance
                elif distance == closest_distance:
                    equidistance = distance
            if closest_distance == equidistance:
                closest_point = None
            """if closest_point is None:
                print(".", end="")
            else:
                if closest_distance > 0:
                    print(string.ascii_lowercase[coords.index(closest_point)], end="")
                else:
                    print(string.ascii_uppercase[coords.index(closest_point)], end="")
"""
            if closest_distance < 10000:
                locations[(x, y)] = closest_point
            if sum_distances < 10000:
                total_safe_area += 1
            if x == min_x or x == max_x or y == min_y or y == max_y:
                points_on_edge.add(closest_point)

    areas_to_count = [coord for coord in coords if coord not in points_on_edge]

    areas = collections.defaultdict(int)

    for _, location in locations.items():
        areas[location] += 1

    areas = {location: area for location, area in areas.items() if location in areas_to_count}

    max_area = max(areas.items(), key=lambda x: x[1])[1]

    if submit_answer:
        submit1(max_area, day=6, year=2018)
        submit2(total_safe_area, day=6, year=2018)
    return max_area, total_safe_area


days[6] = day6
