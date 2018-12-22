from aocd import get_data, submit

import itertools


def day21(submit_answer=False):
    data = get_data(day=21, year=2018).split("\n")
    # Reversed version
    magic = int(data[8].split()[1])
    r3 = 0
    first_check = 0
    last_check = 0
    checks = set()
    while True:
        r1 = r3 | 0x10000
        r3 = magic
        while True:
            r4 = r1 & 0xff
            r3 = r3 + r4
            r3 = r3 & 0xffffff
            r3 = r3 * 65899
            r3 = r3 & 0xffffff
            if 256 > r1:
                break
            for r4 in itertools.count():
                r5 = r4 + 1
                r5 = r5 * 256
                if r5 > r1:
                    break
            r1 = r4
        if first_check == 0:
            first_check = r3
        if r3 not in checks:
            checks.add(r3)
            last_check = r3
        else:
            break

    if submit_answer:
        submit(first_check, 1, day=21, year=2018)
        submit(last_check, 2, day=21, year=2018)
    return first_check, last_check
