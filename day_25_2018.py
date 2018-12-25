from aocd import get_data, submit
import itertools

import re

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) + abs(a[3] - b[3])

def day25(submit_answer=False):
    data = get_data(day=25, year=2018).split("\n")
    answer1 = 0
    answer2 = 0

    points = []
    for line in data:
        x, y, z, w = map(int, re.findall("(-?\d+)", line))
        points.append((x, y, z, w))

    constellations = [[]]

    def is_connected(const_a, const_b):
        for point_a in const_a:
            for point_b in const_b:
                if manhattan_distance(point_a, point_b) <= 3:
                    return True
        return False

    for point in points:
        if len(constellations[-1]) == 0:
            constellations.append([point])
        else:
            connected = False
            for constellation in constellations:
                if is_connected([point], constellation):
                    constellation.append(point)
                    break
            if not connected:  # create new constellation
                constellations.append([point])

    dirty = True
    while dirty:
        dirty = False
        for const_a in constellations:
            for const_b in constellations:
                if const_a is not const_b:
                    if is_connected(const_a, const_b):
                        dirty = True
                        const_a.extend(const_b)
                        const_b.clear()
        if dirty:
            constellations = list(filter(lambda x: len(x) != 0, constellations))

    answer1 = len(constellations)

    if submit_answer:
        submit(answer1, 1, day=25, year=2018)
        submit(answer2, 2, day=25, year=2018)
    return answer1, answer2
