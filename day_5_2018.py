from aocd import get_data, submit1, submit2
from days import days


def reduce(data):
    new_data = []
    while True:
        for i, unit in enumerate(data):
            if i + 1 < len(data) and unit is not None and unit.lower() == data[i + 1].lower() and (unit.isupper() and data[i + 1].islower() or unit.islower() and data[i + 1].isupper()):
                data[i] = None
                data[i + 1] = None
        new_data = [data for data in data if data is not None]
        if len(data) == len(new_data):
            break
        data = new_data
    return data


def day5(submit_answer=False):
    data = get_data(day=5, year=2018)
    answer1 = 0
    answer2 = None

    answer1 = len(reduce(list(data)))

    all_chars = set(data.lower())
    new_length = {}
    for char in all_chars:
        new_data = [c for c in data if c.lower() != char]
        new_length[char] = len(reduce(new_data))

    answer2 = min(new_length.items(), key=lambda x: x[1])

    if submit_answer:
        submit1(answer1, day=5, year=2018)
        submit2(answer2, day=4, year=2018)
    return answer1, answer2


days[5] = day5