from aocd import get_data, submit1, submit2
from days import days
import re
import collections
import itertools


def day3(submit_answer=False):
    data = get_data(day=3, year=2018).split("\n")
    overlap_area = 0
    none_overlap = None

    fabric = collections.defaultdict(int)

    regex = re.compile(r"(\d+)")

    for claim in data:
        groups = regex.findall(claim)
        id, left_edge, top_edge, width, height = map(int, groups)
        for x in range(0, width):
            for y in range(0, height):
                fabric[(x + left_edge, y + top_edge)] += 1

    for num_claims in fabric.values():
        if num_claims > 1:
            overlap_area += 1

    for claim in data:
        groups = regex.findall(claim)
        id, left_edge, top_edge, width, height = map(int, groups)
        failed = False
        for x in range(0, width):
            for y in range(0, height):
                if fabric[(x + left_edge, y + top_edge)] != 1:
                    failed = True
                    break
            if failed:
                break
        if not failed:
            none_overlap = id

    if submit_answer:
        submit1(overlap_area, day=3, year=2018)
        submit2(none_overlap, day=3, year=2018)
    return overlap_area, none_overlap


days[3] = day3
