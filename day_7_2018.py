from aocd import get_data, submit1, submit2
from days import days

import collections
import re
import string


def day7(submit_answer=False):
    data = get_data(day=7, year=2018).split("\n")

    regex = re.compile(r"tep (.)")
    dependencies = collections.defaultdict(list)
    reverse_dependencies = collections.defaultdict(list)
    all_dependencies = set()

    for dep in data:
        dependency, dependent = regex.findall(dep)
        all_dependencies.add(dependent)
        dependencies[dependent].append(dependency)
        reverse_dependencies[dependency].append(dependent)

    zero_dependencies = [step for step in reverse_dependencies.keys() if step not in all_dependencies]
    order = []
    available = list(zero_dependencies)

    while len(available) > 0:
        available.sort()
        current = available.pop(0)
        order.append(current)
        for dependent in reverse_dependencies[current]:
            # If all dependencies are fulfilled
            if all(dependency in order for dependency in dependencies[dependent]):
                available.append(dependent)

    completion_order = "".join(order)

    available = zero_dependencies
    order = []

    workers = [(".", 0)] * 5

    time_elapsed = 0

    while True:
        for i, (current, time) in enumerate(workers):
            if time <= 0:
                if current != ".":
                    order.append(current)
                    for dependent in reverse_dependencies[current]:
                        # If all dependencies are fulfilled
                        if all(dependency in order for dependency in dependencies[dependent]):
                            available.append(dependent)

        for i, (job, time) in enumerate(workers):
            if time <= 0:  # Give them a new job
                available.sort()
                if len(available) > 0:
                    job = available.pop(0)
                    time = string.ascii_uppercase.index(job) + 61
                else:
                    job = "."
                    time = 0
            workers[i] = (job, time - 1)

        have_jobs = any(job != "." for job, time in workers)
        if not have_jobs and len(available) == 0:
            break
        else:
            time_elapsed += 1

    if submit_answer:
        submit1(completion_order, day=7, year=2018)
        submit2(time_elapsed, day=7, year=2018)
    return completion_order, time_elapsed


days[7] = day7
