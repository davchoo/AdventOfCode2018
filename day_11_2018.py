from aocd import get_data, submit
import itertools

import collections


def day11(submit_answer=False):
    data = get_data(day=11, year=2018)

    grid_serial = int(data)

    grid = collections.defaultdict(int)

    for y in range(1, 301):
        for x in range(1, 301):
            rack_id = x + 10
            power_level = rack_id * y + grid_serial
            power_level *= rack_id
            power_level = power_level // 100 % 10
            power_level -= 5
            grid[(x, y)] = power_level

            # Compute 2D Partial Sum Table
            grid[(x, y)] += grid[(x - 1, y)]
            grid[(x, y)] += grid[(x, y - 1)]
            grid[(x, y)] -= grid[(x - 1, y - 1)]  # Remove double count

    max_fuel = 0
    max_fuel_loc = (0, 0)

    for x in range(0, 300-2):
        for y in range(0, 300-2):
            sum_fuel = grid[(x + 3, y + 3)] - grid[(x, y + 3)] - grid[(x + 3, y)] + grid[(x, y)]
            if sum_fuel > max_fuel:
                max_fuel = sum_fuel
                max_fuel_loc = (x + 1, y + 1)

    max_fuel_2 = 0
    max_fuel_loc_2 = (0, 0)
    max_fuel_size_2 = 0

    for x in range(0, 300):
        for y in range(0, 300):
            for size in range(1, 300-max(x, y)):
                sum_fuel = grid[(x + size, y + size)] - grid[(x, y + size)] - grid[(x + size, y)] + grid[(x, y)]
                if sum_fuel > max_fuel_2:
                    max_fuel_2 = sum_fuel
                    max_fuel_loc_2 = (x + 1, y + 1)
                    max_fuel_size_2 = size

    answer1 = f"{max_fuel_loc[0]},{max_fuel_loc[1]}"
    answer2 = f"{max_fuel_loc_2[0]},{max_fuel_loc_2[1]},{max_fuel_size_2}"

    if submit_answer:
        submit(answer1, 1, day=11, year=2018)
        submit(answer2, 2, day=11, year=2018)
    return answer1, answer2
