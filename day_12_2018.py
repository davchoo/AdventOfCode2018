from aocd import get_data, submit


def day12(submit_answer=False):
    data = get_data(day=12, year=2018).split("\n")

    init_state = {i: state for i, state in enumerate(data[0].split()[2])}

    spread = {}
    for s in data[2::]:
        state, __, target = s.split()
        spread[state] = target

    state = init_state.copy()

    diffs = []
    last_plant_count = sum(i for i, pot in state.items() if pot == "#")
    answer1 = 0

    for j in range(0, 2000):
        new_state = {}
        for i in range(-2 + min(state.keys()), 2 + max(state.keys())):
            surroundings = "".join([state[i + o] if i + o in state else "." for o in range(-2, 3)])
            if surroundings in spread:
                new_state[i] = spread[surroundings]
            else:
                if i in state:
                    new_state[i] = "."
        state = new_state
        plant_count = sum(i for i, pot in state.items() if pot == "#")
        if j == 19:
            answer1 = plant_count
        diffs.append(plant_count - last_plant_count)
        last_plant_count = plant_count
        # If the current difference is equal to the previous 2 differences
        if len(diffs) > 3 and diffs[-1] == diffs[-2] and diffs[-1] == diffs[-3]:
            break

    answer2 = (50000000000 - len(diffs)) * diffs[-1] + last_plant_count

    if submit_answer:
        submit(answer1, 1, day=12, year=2018)
        submit(answer2, 2, day=12, year=2018)
    return answer1, answer2
