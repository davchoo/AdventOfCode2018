from aocd import get_data, submit
import itertools

import collections
import re


def day17(submit_answer=False):
    data = get_data(day=17, year=2018).split("\n")

    scan = collections.defaultdict(lambda: ".")

    for line in data:
        axis1, pos1, axis2, pos2, pos3 = re.match("(.)=(\d+), (.)=(\d+)\.\.(\d+)", line).groups()
        pos1 = int(pos1)
        pos2 = int(pos2)
        pos3 = int(pos3)
        if axis1 == "x":
            x_range = range(pos1, pos1 + 1)
            y_range = range(pos2, pos3 + 1)
        else:
            x_range = range(pos2, pos3 + 1)
            y_range = range(pos1, pos1 + 1)
        for x in x_range:
            for y in y_range:
                scan[(x, y)] = "#"

    max_x = max(scan.keys(), key=lambda x: x[0])[0]
    max_y = max(scan.keys(), key=lambda x: x[1])[1]
    min_x = min(scan.keys(), key=lambda x: x[0])[0]
    min_y = min(scan.keys(), key=lambda x: x[1])[1]

    def water_fall(x, y):
        lowest_y = y
        for new_y in range(y, max_y+1):
            if scan[(x, new_y)] == "#" or scan[(x, new_y)] == "~":
                lowest_y = new_y-1
                break
            elif scan[(x, new_y)] == "|" and new_y != y:
                return False
            else:
                if new_y >= min_y:
                    scan[(x, new_y)] = "|"
        if lowest_y == y:  # we hit max y
            return
        for new_y in range(lowest_y, y-1, -1):
            left = min_x
            left_open = False
            right = max_x
            right_open = False

            for new_x in range(x, min_x-5, -1):
                if scan[(new_x, new_y)] == "#":
                    left = new_x + 1
                    break
                else:
                    scan[(new_x, new_y)] = "|"
                    if scan[(new_x, new_y+1)] == "." or scan[(new_x, new_y+1)] == "|":
                        left = new_x
                        left_open = True
                        break
            for new_x in range(x+1, max_x+5):
                if scan[(new_x, new_y)] == "#":
                    right = new_x - 1
                    break
                else:
                    scan[(new_x, new_y)] = "|"
                    if scan[(new_x, new_y+1)] == "." or scan[(new_x, new_y+1)] == "|":
                        right = new_x
                        right_open = True
                        break
            if not left_open and not right_open:
                for new_x in range(left, right+1):
                    scan[(new_x, new_y)] = "~"
            else:
                reached_height = False
                if left_open:
                    reached_height = water_fall(left, new_y)
                if right_open:
                    reached_height = reached_height or water_fall(right, new_y)
                if not reached_height:
                    return new_y == y
        return True
    scan[(500, 0)] = "+"

    water_fall(500, 0)

    counts = collections.Counter(scan.values())
    answer1 = counts["~"] + counts["|"]
    answer2 = counts["~"]

    if submit_answer:
        submit(answer1, 1, day=17, year=2018)
        submit(answer2, 2, day=17, year=2018)
    return answer1, answer2
