from aocd import get_data, submit

import collections
import re

import re


def addr(registers, a, b, c):
    registers[c] = registers[a] + registers[b]


def addi(registers, a, b, c):
    registers[c] = registers[a] + b


def mulr(registers, a, b, c):
    registers[c] = registers[a] * registers[b]


def muli(registers, a, b, c):
    registers[c] = registers[a] * b


def banr(registers, a, b, c):
    registers[c] = registers[a] & registers[b]


def bani(registers, a, b, c):
    registers[c] = registers[a] & b


def borr(registers, a, b, c):
    registers[c] = registers[a] | registers[b]


def bori(registers, a, b, c):
    registers[c] = registers[a] | b


def setr(registers, a, b, c):
    registers[c] = registers[a]


def seti(registers, a, b, c):
    registers[c] = a


def gtir(registers, a, b, c):
    if a > registers[b]:
        registers[c] = 1
    else:
        registers[c] = 0


def gtri(registers, a, b, c):
    if registers[a] > b:
        registers[c] = 1
    else:
        registers[c] = 0


def gtrr(registers, a, b, c):
    if registers[a] > registers[b]:
        registers[c] = 1
    else:
        registers[c] = 0


def eqir(registers, a, b, c):
    if a == registers[b]:
        registers[c] = 1
    else:
        registers[c] = 0


def eqri(registers, a, b, c):
    if registers[a] == b:
        registers[c] = 1
    else:
        registers[c] = 0


def eqrr(registers, a, b, c):
    if registers[a] == registers[b]:
        registers[c] = 1
    else:
        registers[c] = 0


def day19(submit_answer=False):
    data = get_data(day=19, year=2018).split("\n")
    answer1 = 0

    opcodes = {"addr": addr, "addi": addi,
               "mulr": mulr, "muli": muli,
               "banr": banr, "bani": bani,
               "borr": borr, "bori": bori,
               "setr": setr, "seti": seti,
               "gtir": gtir, "gtri": gtri, "gtrr": gtrr,
               "eqir": eqir, "eqri": eqri, "eqrr": eqrr}

    registers = [0] * 6
    ip_register = int(re.findall("(\d)+", data[0])[0])
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

    number = registers[3]

    answer2 = 0
    for factor in range(1, number + 1):
        if number % factor == 0:
            answer2 += factor

    if submit_answer:
        submit(answer1, 1, day=19, year=2018)
        submit(answer2, 2, day=19, year=2018)
    return answer1, answer2
