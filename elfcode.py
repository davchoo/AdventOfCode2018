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


opcodes = {"addr": addr, "addi": addi,
           "mulr": mulr, "muli": muli,
           "banr": banr, "bani": bani,
           "borr": borr, "bori": bori,
           "setr": setr, "seti": seti,
           "gtir": gtir, "gtri": gtri, "gtrr": gtrr,
           "eqir": eqir, "eqri": eqri, "eqrr": eqrr}