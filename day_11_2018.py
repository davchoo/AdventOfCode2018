from aocd import get_data, submit
import itertools

import collections


def day11(submit_answer=False):
    data = get_data(day=11, year=2018)

    grid_serial = int(data)

    grid = collections.defaultdict(int)

    for x in range(1, 301):
        for y in range(1, 301):
            rack_id = x + 10
            power_level = rack_id * y + grid_serial
            power_level *= rack_id
            power_level = power_level // 100 % 10
            power_level -= 5
            grid[(x, y)] = power_level

    max_fuel = 0
    max_fuel_loc = (0, 0)

    for x in range(1, 301):
        for y in range(1, 301):
            if x+3 > 300 or y+3 > 300:
                break
            sum_fuel = 0
            for ox in range(0, 3):
                for oy in range(0, 3):
                    sum_fuel += grid[(x + ox, y + oy)]
            if sum_fuel > max_fuel:
                max_fuel = sum_fuel
                max_fuel_loc = (x, y)

    max_fuel_2 = 0
    max_fuel_loc_2 = (0, 0)
    max_fuel_size_2 = 0

    for x in range(1, 301):
        for y in range(1, 301):
            sum_fuel = grid[(x, y)]
            for size in range(1, 300-max(x-1, y-1)):
                for o in range(0, size-1):
                    sum_fuel += grid[(x + o, y + size - 1)]
                    sum_fuel += grid[(x + size - 1, y + o)]
                if size > 1:
                    sum_fuel += grid[(x + size - 1, y + size - 1)]
                if sum_fuel > max_fuel_2:
                    max_fuel_2 = sum_fuel
                    max_fuel_loc_2 = (x, y)
                    max_fuel_size_2 = size

    answer2 = f"{max_fuel_loc_2[0]},{max_fuel_loc_2[1]},{max_fuel_size_2}"

    if submit_answer:
        submit(max_fuel_loc, 1, day=11, year=2018)
        submit(answer2, 2, day=11, year=2018)
    return max_fuel_loc, answer2
