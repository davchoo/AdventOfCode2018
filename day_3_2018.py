from aocd import get_data, submit1, submit2
from days import days
import re
import itertools


def day3(submit_answer=False):
    data = get_data(day=3, year=2018).split("\n")
    answer1 = 0
    answer2 = None

    map = [[0 for i in range(1000)] for j in range(1000)]

    regex = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")

    for claim in data:
        groups = regex.match(claim)
        id, left_edge, top_edge, width, height = groups.group(1), groups.group(2), groups.group(3), groups.group(4), groups.group(5)
        id = int(id)
        left_edge = int(left_edge)
        top_edge = int(top_edge)
        width = int(width)
        height = int(height)
        for x in range(0, width):
            for y in range(0, height):
                map[x + left_edge][y + top_edge] += 1

    for claim in data:
        groups = regex.match(claim)
        id, left_edge, top_edge, width, height = groups.group(1), groups.group(2), groups.group(3), groups.group(4), groups.group(5)
        id = int(id)
        left_edge = int(left_edge)
        top_edge = int(top_edge)
        width = int(width)
        height = int(height)
        failed = False
        for x in range(0, width):
            for y in range(0, height):
                if map[x + left_edge][y + top_edge] != 1:
                    failed = True
                    break
            if failed:
                break
        if not failed:
            answer2 = id

    for x in range(1000):
        for y in range(1000):
            if map[x][y] > 1:
                answer1 += 1

    if submit_answer:
        submit1(answer1, day=3, year=2018)
        submit2(answer2, day=3, year=2018)
    return answer1, answer2


days[3] = day3
