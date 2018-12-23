from aocd import get_data, submit
import itertools

import re
from z3 import *


def day23(submit_answer=False):
    data = get_data(day=23, year=2018).split("\n")
    dist_to_max = 0
    nanobots = []

    def manhattan(pos1, pos2):
        return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1]) + abs(pos2[2] - pos1[2])

    for line in data:
        x, y, z, r = map(int, re.findall("(-?\\d+)", line))
        nanobots.append(((x, y, z), r))

    strongest_bot = max(nanobots, key=lambda x: x[1])
    in_range_bots = 0
    for pos, r in nanobots:
        distance = manhattan(pos, strongest_bot[0])
        if distance <= strongest_bot[1]:
            in_range_bots += 1

    # Black magic coming up

    def z3_abs(x):
        return If(x >= 0, x, -x)

    def z3_manhattan(pos1, pos2):
        return z3_abs(pos2[0] - pos1[0]) + z3_abs(pos2[1] - pos1[1]) + z3_abs(pos2[2] - pos1[2])

    x, y, z = Ints("x y z")
    target = (x, y, z)
    bots_in_range_expr = x * 0
    for pos, r in nanobots:
        bots_in_range_expr += If(z3_manhattan(target, pos) <= r, 1, 0)

    optimize = Optimize()
    optimize.maximize(bots_in_range_expr)
    optimize.minimize(z3_manhattan(target, (0, 0, 0)))

    if optimize.check():
        model = optimize.model()
        dist_to_max = manhattan((model[x].as_long(), model[y].as_long(), model[z].as_long()), (0, 0, 0))

    if submit_answer:
        submit(in_range_bots, 1, day=23, year=2018)
        submit(dist_to_max, 2, day=23, year=2018)
    return in_range_bots, dist_to_max
