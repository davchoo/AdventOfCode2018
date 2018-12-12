from aocd import get_data, submit

import re


def day10(submit_answer=False):
    data = get_data(day=10, year=2018).split("\n")

    regex = re.compile(r"(-?\d+)")

    points = []

    for point in data:
        pos_x, pos_y, vel_x, vel_y = map(int, regex.findall(point))
        points.append((pos_x, pos_y, vel_x, vel_y))

    current_time = 0
    last_sky = {}
    last_width = 1000

    while True:
        sky = {}
        for pos_x, pos_y, vel_x, vel_y in points:
            sky[(pos_x + vel_x * current_time, pos_y + vel_y * current_time)] = True

        min_x = min(sky.keys(), key=lambda x: x[0])[0]
        max_x = max(sky.keys(), key=lambda x: x[0])[0]

        width = max_x - min_x

        # Print the previous sky if the width of the sky starts growing
        if last_width < width and last_width < 1000:
            min_x = min(last_sky.keys(), key=lambda x: x[0])[0]
            min_y = min(last_sky.keys(), key=lambda x: x[1])[1]
            max_x = max(last_sky.keys(), key=lambda x: x[0])[0]
            max_y = max(last_sky.keys(), key=lambda x: x[1])[1]

            answer1 = "\n\t\t"
            for y in range(min_y, max_y + 1):
                for x in range(min_x, max_x+1):
                    if (x, y) in last_sky:
                        answer1 += "#"
                    else:
                        answer1 += " "
                answer1 += "\n\t\t"
            current_time -= 1  # The time during the previous cycle
            break
        else:
            last_width = width
            last_sky = sky
        current_time += 1
    if submit_answer:
        submit(current_time, 2, day=10, year=2018)
    return answer1, current_time
