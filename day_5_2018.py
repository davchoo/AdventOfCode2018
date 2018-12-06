from aocd import get_data, submit1, submit2
from days import days


def reduce(data):
    while True:
        previous_length = len(data)
        for i, unit in enumerate(data):
            if i + 1 < len(data):  # Next unit is outside polymer
                if unit is not None:  # Skip if already eliminated
                    next_unit = data[i + 1]
                    if unit.lower() == next_unit.lower() and unit != next_unit:  # Same unit, but different polarity
                        data[i] = None
                        data[i + 1] = None
        data = [d for d in data if d is not None]
        if previous_length == len(data):
            return data


def day5(submit_answer=False):
    data = get_data(day=5, year=2018)

    reduced_length = len(reduce(list(data)))

    all_units = set(data.lower())
    new_reduced_lengths = {}
    for char in all_units:
        new_data = [c for c in data if c.lower() != char]
        new_reduced_lengths[char] = len(reduce(new_data))

    fully_reduced = min(new_reduced_lengths.items(), key=lambda x: x[1])[1]

    if submit_answer:
        submit1(reduced_length, day=5, year=2018)
        submit2(fully_reduced, day=5, year=2018)
    return reduced_length, fully_reduced


days[5] = day5
