from aocd import get_data, submit
import itertools


def find_repeating_freq(delta_frequency):
    found_frequencies = set()
    frequency = 0
    for delta in itertools.cycle(delta_frequency):
        frequency += delta
        if frequency not in found_frequencies:
            found_frequencies.add(frequency)
        else:
            return frequency


def day1(submit_answer=False):
    data = get_data(day=1, year=2018)
    delta_frequency = list(map(int, data.split("\n")))
    total_frequency = sum(delta_frequency)
    repeating_frequency = find_repeating_freq(delta_frequency)

    if submit_answer:
        submit(total_frequency, 1, day=1, year=2018)
        submit(repeating_frequency, 2, day=1, year=2018)
    return total_frequency, repeating_frequency
