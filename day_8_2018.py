from aocd import get_data, submit
from days import days

import collections
import itertools
import re
import sys


def day8(submit_answer=False):
    data = get_data(day=8, year=2018).split(" ")

    regex = re.compile(r"(\d+)")

    data = list(map(int, data))

    parents = [[data.pop(0), data.pop(0), [], None]]

    sum_metadata = 0

    while len(data) > 0:
        if len(parents[0][2]) < parents[0][0]:
            current = [data.pop(0), data.pop(0), [], None]
            parents.insert(0, current)
        else:
            parents[0][3] = [data.pop(0) for i in range(parents[0][1])]
            sum_metadata += sum(parents[0][3])
            if len(parents) == 1:
                break
            parents[1][2].append(parents[0])
            parents.pop(0)

    def get_value(node):
        value = 0
        if len(node[2]) > 0:
            for index in node[3]:
                if index != 0 and (index - 1) < len(node[2]):
                    value += get_value(node[2][index - 1])
        else:
            value = sum(node[3])
        return value

    answer2 = get_value(parents[0])

    if submit_answer:
        submit(sum_metadata, 1, day=8, year=2018)
        submit(answer2, 2, day=8, year=2018)
    return sum_metadata, answer2


days[8] = day8
