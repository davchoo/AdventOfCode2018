from aocd import get_data, submit

import re

from elfcode import *


def day19(submit_answer=False):
    data = get_data(day=19, year=2018).split("\n")

    registers = [0] * 6
    ip_register = int(re.findall("(\\d)+", data[0])[0])
    program_data = data[1::]

    for i, line in enumerate(program_data):
        opcode, *args = line.split()
        program_data[i] = (opcode, *map(int, args))

    while registers[ip_register] < len(program_data):
        opcode, *args = program_data[registers[ip_register]]
        opcodes[opcode](registers, *args)
        registers[ip_register] += 1

    answer1 = registers[0]

    registers = [0] * 6
    registers[0] = 1

    while registers[0] != 0:
        opcode, *args = program_data[registers[ip_register]]
        opcodes[opcode](registers, *args)
        registers[ip_register] += 1

    number = max(registers)

    answer2 = 0
    for factor in range(1, number + 1):
        if number % factor == 0:
            answer2 += factor

    if submit_answer:
        submit(answer1, 1, day=19, year=2018)
        submit(answer2, 2, day=19, year=2018)
    return answer1, answer2
