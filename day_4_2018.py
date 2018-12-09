from aocd import get_data, submit1, submit2
import re
import collections
import itertools
from operator import itemgetter


def day4(submit_answer=False):
    data = sorted(get_data(day=4, year=2018).split("\n"))
    answer1 = 0
    answer2 = None

    regex = re.compile(r"(\d+)")

    guards = collections.defaultdict(int)
    guard_total_sleep = collections.defaultdict(int)

    current_guard = 0
    last_minute = 0

    for action in data:
        if "begins shift" in action:
            year, month, day, hr, minute, current_guard = map(int, regex.findall(action))
            last_minute = 0
        else:
            year, month, day, hr, minute = map(int, regex.findall(action))
            if "wakes" in action:
                for i in range(last_minute, minute):
                    guards[(current_guard, i)] += 1
                    guard_total_sleep[current_guard] += 1
            last_minute = minute

    id_of_max_slept = max(guard_total_sleep.items(), key=lambda x: x[1])[0]

    minute_of_max_overlap = max([(min, overlap) for (id, min), overlap in guards.items() if id == id_of_max_slept], key=lambda x: x[1])[0]

    answer1 = id_of_max_slept * minute_of_max_overlap
    (id_of_max_overlaps, minute_of_max_overlap), overlaps = max(guards.items(), key=lambda x: x[1])

    answer2 = id_of_max_overlaps * minute_of_max_overlap

    if submit_answer:
        submit1(answer1, day=4, year=2018)
        submit2(answer2, day=4, year=2018)
    return answer1, answer2
