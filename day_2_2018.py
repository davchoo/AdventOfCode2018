from aocd import get_data, submit1, submit2
from days import days
import itertools


def day2(submit_answer=False):
    data = get_data(day=2, year=2018).split("\n")
    doubles = 0
    triples = 0
    for box_id in data:
        box_id = list(box_id)
        unique_chars = set(box_id)
        already_double = False
        already_triple = False
        for char in unique_chars:
            count = box_id.count(char)
            if count == 2 and not already_double:
                doubles += 1
                already_double = True
            if count == 3 and not already_triple:
                triples += 1
                already_triple = True
    checksum = doubles * triples

    common = None
    
    for a in data:
        for b in data:
            diffs = 0
            diff_pos = 0
            i = 0
            for pair in zip(a, b):
                char_a, char_b = pair
                if char_a != char_b:
                    diffs += 1
                    diff_pos = i
                    if diffs > 1:
                        break
                i += 1
            if diffs == 1:
                common = list(a)
                del common[diff_pos]
                common = "".join(common)

    if submit_answer:
        submit1(checksum, day=2, year=2018)
        submit2(common, day=2, year=2018)
    return checksum, common


days[2] = day2
