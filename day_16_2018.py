from aocd import get_data, submit

import collections
import re

from elfcode import *


def day16(submit_answer=False):
    data = get_data(day=16, year=2018).split("\n")
    answer1 = 0
    states = []

    for i in range(0, len(data), 4):
        before, code, after = data[i:i+3]
        if "Before" not in before:  # in second section
            break
        before = list(map(int, re.findall("(\\d+)", before)))
        after = list(map(int, re.findall("(\\d+)", after)))
        code = list(map(int, code.split()))
        states.append((before, code, after))

    test_program = []

    for i in range(len(states) * 4 + 2, len(data)):
        opcode, a, b, c = map(int, data[i].split())
        test_program.append((opcode, a, b, c))

    opcode_map = collections.defaultdict(lambda: {"potential": {}})

    for before, code, after in states:
        potential_opcodes = 0
        for name, func in opcodes.items():
            registers = before[:]
            opcode, *args = code
            func(registers, *args)
            if registers == after:
                potential_opcodes += 1
                if name not in opcode_map[opcode]["potential"]:
                    opcode_map[opcode]["potential"][name] = []
                opcode_map[opcode]["potential"][name].append((before, code, after))
        if potential_opcodes >= 3:
            answer1 += 1

    def remove_potential(opcode):
        for current_opcode, d in opcode_map.items():
            if opcode in d["potential"]:
                del d["potential"][opcode]

    while any(len(d["potential"]) > 0 for opcode, d in opcode_map.items()):
        for opcode, d in opcode_map.items():
            if len(d["potential"]) == 1:
                actual_opcode = next(iter(d["potential"].keys()))
                d["is"] = actual_opcode
                remove_potential(actual_opcode)

    opcode_map = {opcode: opcodes[d["is"]] for opcode, d in opcode_map.items()}

    registers = [0, 0, 0, 0]

    for opcode, *args in test_program:
        opcode_map[opcode](registers, *args)

    answer2 = registers[0]

    if submit_answer:
        submit(answer1, 1, day=16, year=2018)
        submit(answer2, 2, day=16, year=2018)
    return answer1, answer2
