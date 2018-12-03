from aocd import get_data, submit1, submit2
from days import days
import itertools


def day3(submit_answer=False):
    data = get_data(day=3, year=2018).split("\n")
    answer1 = None
    answer2 = None

    if submit_answer:
        submit1(answer1, day=3, year=2018)
        submit2(answer2, day=3, year=2018)
    return answer1, answer2


days[3] = day3
