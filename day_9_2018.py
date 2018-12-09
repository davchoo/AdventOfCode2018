from aocd import get_data, submit

import collections
import itertools
import re
import sys


def max_score(players, last_marble):
    marbles = collections.deque([0])

    current_player = 0
    scores = collections.defaultdict(int)
    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            # print(f"Player {current_player} grabbed a multiple of 23, {marble}. Current pos: {current_pos}")
            marbles.rotate(7)
            scores[current_player] += marble + marbles.pop()
            marbles.rotate(-1)
        else:
            # print(f"Player {current_player} placed {marble}. Current pos: {current_pos} New pos {new_pos}")
            marbles.rotate(-1)
            marbles.append(marble)
        current_player = (current_player + 1) % players

    return max(scores.values())


def day9(submit_answer=False):
    data = get_data(day=9, year=2018)

    players, last_marble = list(map(int, re.findall("(\d+)", data)))

    answer1 = max_score(players, last_marble)

    answer2 = max_score(players, last_marble * 100)

    if submit_answer:
        submit(answer1, 1, day=9, year=2018)
        submit(answer2, 2, day=9, year=2018)
    return answer1, answer2
