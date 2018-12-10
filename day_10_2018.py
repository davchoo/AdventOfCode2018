from aocd import get_data, submit

import collections
import itertools
import re
import sys


def day10(submit_answer=False):
    data = get_data(day=10, year=2018).split("\n")
    answer1 = 0
    answer2 = 0

    regex = re.compile(r"(-?\d+)")

    points = []

    # y neg up

    for point in data:
        pos_x, pos_y, vel_x, vel_y = map(int, regex.findall(point))
        points.append((pos_x, pos_y, vel_x, vel_y))

    i = 0
    last_under = -1
    last_map = {}
    last_width = 1000

    while True:
        for j, (pos_x, pos_y, vel_x, vel_y) in enumerate(points):
            points[j] = (pos_x + vel_x, pos_y + vel_y, vel_x, vel_y)
        m = {}
        for pos_x, pos_y, *rest in points:
            m[(pos_x, pos_y)] = True

        min_x = min(m.keys(), key=lambda x: x[0])[0]
        max_x = max(m.keys(), key=lambda x: x[0])[0]

        width = max_x - min_x

        if last_width < width and last_width < 1000:
            min_x = min(last_map.keys(), key=lambda x: x[0])[0]
            min_y = min(last_map.keys(), key=lambda x: x[1])[1]
            max_x = max(last_map.keys(), key=lambda x: x[0])[0]
            max_y = max(last_map.keys(), key=lambda x: x[1])[1]
            print(f"Time: {i} {width}")

            answer1 = "\n\t\t"
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x+1):
                    if (x, y) in last_map:
                        answer1 += "#"
                    else:
                        answer1 += " "
                answer1 += "\n\t\t"
            break
        else:
            last_width = width
            last_map = m
        i += 1
    if submit_answer:
        submit(i, 2, day=10, year=2018)
    return answer1, i
