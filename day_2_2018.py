import itertools

from aocd import get_data, submit1, submit2

from collections import Counter
from itertools import compress


def box_checksum(boxes):
    doubles = 0
    triples = 0
    for box_id in boxes:
        counts = Counter(box_id).values()
        if 2 in counts:
            doubles += 1
        if 3 in counts:
            triples += 1
    return doubles * triples


def find_common_box_id(boxes):
    for a, b in itertools.combinations(boxes, 2):
        similar = [char_a == char_b for char_a, char_b in zip(a, b)]
        if similar.count(False) == 1:  # Only 1 differing character
            return "".join(compress(a, similar))


def day2(submit_answer=False):
    data = get_data(day=2, year=2018).split("\n")

    checksum = box_checksum(data)
    common_id = find_common_box_id(data)

    if submit_answer:
        submit1(checksum, day=2, year=2018)
        submit2(common_id, day=2, year=2018)
    return checksum, common_id

