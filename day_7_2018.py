from aocd import get_data, submit1, submit2
from days import days

import collections
import re
import string

def day7(submit_answer=False):
    data = get_data(day=7, year=2018).split("\n")

    regex = re.compile(r"tep (.)")
    answer1 = 0
    answer2 = 0

    dependencies = collections.defaultdict(list)
    dependencies2 = collections.defaultdict(list)
    steps = set()
    next_step = set()

    for dep in data:
        first, then = regex.findall(dep)
        steps.add(first)
        next_step.add(then)
        dependencies[then].append(first)
        dependencies2[first].append(then)

    no_deps = [step for step in dependencies2.keys() if step not in next_step]

    no_deps.sort()

    order = []

    available = list(no_deps)

    while len(available) > 0:
        available.sort()
        current = available.pop(0)
        order.append(current)
        for dependent in dependencies2[current]:
            fulfilled = True
            for dependency in dependencies[dependent]:
                if dependency not in order:
                    fulfilled = False
                    break
            if fulfilled:
                available.append(dependent)

    answer1 = "".join(order)

    available = no_deps
    order = []

    workers = [(".", 0)] * 5

    time_elapsed = 0

    while True:
        for i, (current, time) in enumerate(workers):
            if time <= 0:
                if current != ".":
                    order.append(current)
                    for dependent in dependencies2[current]:
                        fulfilled = True
                        for dependency in dependencies[dependent]:
                            if dependency not in order:
                                fulfilled = False
                                break
                        if fulfilled:
                            available.append(dependent)

        for i, (current, time) in enumerate(workers):
            if time <= 0:
                available.sort()
                if len(available) > 0:
                    new = available.pop(0)
                    workers[i] = (new, string.ascii_uppercase.index(new) + 61)
                else:
                    workers[i] = (".", 0)
        for i, (job, time) in enumerate(workers):
            workers[i] = (job, time - 1)

        have_jobs = False
        total_time_left = 0
        for job, time in workers:
            if job != ".":
                total_time_left += time
                have_jobs = True
        if not have_jobs and len(available) == 0:
            break
        else:
            time_elapsed += 1

    answer2 = time_elapsed

    if submit_answer:
        submit1(answer1, day=7, year=2018)
        #submit2(answer2, day=7, year=2018)
    return answer1, answer2


days[7] = day7
