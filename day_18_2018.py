from aocd import get_data, submit

import collections


def day18(submit_answer=False):
    data = get_data(day=18, year=2018).split("\n")

    adjacent = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

    scan = collections.defaultdict(lambda: "O", {(x, y): c for y, line in enumerate(data) for x, c in enumerate(line)})
    all_resource_values = []
    repeating_vals = []
    repeating_index = 0
    for i in range(1000):
        counts = collections.Counter(scan.values())
        resource_value = counts["|"] * counts["#"]
        if resource_value in all_resource_values:
            if repeating_index == 0:
                repeating_index = i  # The start of the cycle
            if resource_value not in repeating_vals:
                repeating_vals.append(resource_value)
            else:
                break  # Found the cycle
        else:
            repeating_vals = []  # Skips any single repeats
            repeating_index = 0
        all_resource_values.append(counts["|"] * counts["#"])
        new_scan = collections.defaultdict(lambda: "O")
        for y in range(0, len(data)):
            for x in range(0, len(data[0])):
                current = scan[(x, y)]
                if current == "O":
                    continue
                surroundings = collections.Counter(scan[(x + x_off, y + y_off)] for x_off, y_off in adjacent)
                new = current
                if current == "." and surroundings["|"] >= 3:
                    new = "|"
                elif current == "|" and surroundings["#"] >= 3:
                    new = "#"
                elif current == "#":
                    if not (surroundings["#"] >= 1 and surroundings["|"] >= 1):
                        new = "."
                new_scan[(x, y)] = new
        scan = new_scan

    answer1 = all_resource_values[10]
    answer2 = repeating_vals[(1000000000 - repeating_index) % 28]

    if submit_answer:
        submit(answer1, 1, day=18, year=2018)
        submit(answer2, 2, day=18, year=2018)
    return answer1, answer2
