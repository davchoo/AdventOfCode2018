from aocd import get_data, submit


def day12(submit_answer=False):
    data = get_data(day=12, year=2018).split("\n")

    init_state = {}
    for i, state in enumerate(data[0].split()[2]):
        init_state[i] = state

    spread_data = data[2::]

    spread = {}

    for s in spread_data:
        state, __, target = s.split()
        spread[state] = target

    state = init_state.copy()

    for j in range(1, 21):
        new_state = {}
        for i in range(-2+min(state.keys()), 2+max(state.keys())):
            surroundings = "".join([state[i+o] if o+i in state else "." for o in range(-2, 3)])
            if surroundings in spread:
                new_state[i] = spread[surroundings]
            else:
                if i in state:
                    new_state[i] = "."
        state = new_state

    answer1 = sum(i for i, pot in state.items() if pot == "#")

    state = init_state.copy()

    diffs = []
    last_plant_count = 0

    for k, v in state.items():
        if v == "#":
            last_plant_count += k

    for j in range(1, 2000+1):
        new_state = {}
        for i in range(-2 + min(state.keys()), 2 + max(state.keys())):
            surroundings = "".join([state[i + o] if o + i in state else "." for o in range(-2, 3)])
            if surroundings in spread:
                new_state[i] = spread[surroundings]
            else:
                if i in state:
                    new_state[i] = "."
        state = new_state
        plant_count = sum(i for i, pot in state.items() if pot == "#")
        diffs.append(plant_count - last_plant_count)
        last_plant_count = plant_count
        if len(diffs) > 3 and diffs[-1] == diffs[-2] and diffs[-1] == diffs[-3]:
            break

    answer2 = (50000000000 - len(diffs)) * diffs[-1] + last_plant_count

    if submit_answer:
        submit(answer1, 1, day=12, year=2018)
        submit(answer2, 2, day=12, year=2018)
    return answer1, answer2
