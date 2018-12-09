from aocd import get_data, submit
import itertools


def day1(submit_answer=False):
    data = get_data(day=1, year=2018)
    total_frequency = 0
    frequencies = list(map(int, data.split("\n")))

    for f in frequencies:
        total_frequency += f

    found_frequencies = set()
    frequency = 0
    for f in itertools.cycle(frequencies):
        frequency += f
        if frequency not in found_frequencies:
            found_frequencies.add(frequency)
        else:
            break
    if submit_answer:
        submit(total_frequency, 1, day=1, year=2018)
        submit(frequency, 2, day=1, year=2018)
    return total_frequency, frequency
