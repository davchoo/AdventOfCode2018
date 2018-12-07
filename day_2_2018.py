from aocd import get_data, submit1, submit2
from days import days

from collections import Counter
from itertools import compress


def day2(submit_answer=False):
    data = get_data(day=2, year=2018).split("\n")
    doubles = 0
    triples = 0
    for box_id in data:
        counts = Counter(box_id).values()
        if 2 in counts:
            doubles += 1
        if 3 in counts:
            triples += 1
    checksum = doubles * triples

    common = None
    
    for a in data:
        for b in data:
            similar = [char_a == char_b for char_a, char_b in zip(a, b)]
            if similar.count(False) == 1:  # Only 1 differing character
                common = "".join(list(compress(a, similar)))
                break
        if common is not None:
            break

    if submit_answer:
        submit1(checksum, day=2, year=2018)
        submit2(common, day=2, year=2018)
    return checksum, common


days[2] = day2
