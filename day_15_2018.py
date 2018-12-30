from aocd import get_data, submit

import collections
import copy


def draw(world, units, debug={}):
    occupied = {}
    for unit in units:
        occupied[unit["pos"]] = True

    min_x = min(world.keys(), key=lambda x: x[0])[0]
    min_y = min(world.keys(), key=lambda x: x[1])[1]
    max_x = max(world.keys(), key=lambda x: x[0])[0]
    max_y = max(world.keys(), key=lambda x: x[1])[1]
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if isinstance(debug, dict) and (x, y) in debug:
                print(debug[(x, y)], end="")
            elif callable(debug) and debug(x, y) != ".":
                print(debug(x, y), end="")
            elif (x, y) in occupied:
                for unit in units:
                    if unit["pos"] == (x, y):
                        print(unit["type"], end="")
            else:
                print(world[(x, y)], end="")
        for i, unit in enumerate(units):
            if unit["pos"][1] == y:
                print(f" {unit['type']}[{i}]{unit['pos']}({unit['hp']}) ", end="")
        print()
    print()


directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def simulate(world, goblins, elfs):
    def get_occupied():
        occupied = collections.defaultdict(lambda: False)
        units = goblins + elfs
        for unit in units:
            if unit["hp"] > 0:
                occupied[unit["pos"]] = True
        return occupied

    def get_all_costs(start):
        occupied = get_occupied()
        costs = collections.defaultdict(lambda: 1e100)
        parents = collections.defaultdict(lambda x: [], {start: [start]})
        open = collections.OrderedDict({start: 0})
        while len(open) > 0:
            pos, current_cost = open.popitem()
            costs[pos] = current_cost

            new_cost = current_cost + 1
            for x_off, y_off in directions:
                new_pos = (pos[0] + x_off, pos[1] + y_off)
                if world[new_pos] == "." and not occupied[new_pos]:
                    cost = costs[new_pos]
                    if new_pos in open:
                        cost = min(cost, open[new_pos])
                    if cost == new_cost:
                        parents[new_pos].append(pos)
                    elif new_cost < cost:
                        parents[new_pos] = [pos]
                        open[new_pos] = new_cost

        return costs, parents

    # Returns True if unit could attack
    def attack(unit, targets):
        x, y = unit["pos"]
        adjacent = [(x + x_off, y + y_off) for x_off, y_off in directions]
        in_range = [unit for unit in targets if unit["pos"] in adjacent and unit["hp"] > 0]
        in_range = sorted(in_range, key=lambda x: (x["hp"], x["pos"][1], x["pos"][0]))

        if len(in_range) > 0:
            # print(f"\t\tUnit {unit['type']}[{i}]{unit['pos']}({unit['hp']}) wants to fight.")
            # print(f"\t\tUnit {unit['type']}[{i}]{unit['pos']}({unit['hp']}) has {len(in_range)} possible targets.")
            target = in_range[0]
            # print(f"\t\tUnit {unit['type']}[{i}]{unit['pos']}({unit['hp']}) decides to fight: {target['type']}[{i}]{target['pos']}({target['hp']})")
            target["hp"] -= unit["attack_power"]
            if target["hp"] <= 0:  # Killed, shouldn't exist on map
                occupied[target["pos"]] = False
            return True
        return False

    # Returns True if unit have moved
    def move(unit, targets):
        costs, parents = get_all_costs(unit["pos"])
        # print(f"\t\tUnit {unit['type']}[{i}]{unit['pos']}({unit['hp']}) wants to move.")
        target_adjacent = []

        for target in targets:
            x, y = target["pos"]
            for x_off, y_off in directions:
                new_x = x + x_off
                new_y = y + y_off
                # Not a wall, not a unit and reachable
                if world[(new_x, new_y)] == "." and not occupied[(new_x, new_y)] and (new_x, new_y) in costs:
                    target_adjacent.append((new_x, new_y))

        target_adjacent = sorted(target_adjacent, key=lambda x: (costs[x], x[1], x[0]))

        if len(target_adjacent) == 0:
            # print(f"\t\tUnit {unit['type']}[{i}]{unit['pos']}({unit['hp']}) has nowhere to move to.")
            return False

        path = [target_adjacent[0]]
        current = sorted(parents[target_adjacent[0]], key=lambda x: (x[1], x[0]))[0]
        while current != unit["pos"]:
            path.append(current)
            current = sorted(parents[current], key=lambda x: (x[1], x[0]))[0]
        occupied[unit["pos"]] = False
        unit["pos"] = path[-1]
        occupied[unit["pos"]] = True
        return True

    current_round = 0
    while len(goblins) > 0 and len(elfs) > 0:
        current_round += 1
        # print("Starting round.")
        units = sorted(goblins + elfs, key=lambda x: (x["pos"][1], x["pos"][0]))
        occupied = get_occupied()

        for i, unit in enumerate(units):
            if unit["hp"] <= 0:
                continue
            # print(f"\tUnit {i} takes a turn.")
            targets = goblins
            if unit["type"] == "G":
                targets = elfs

            if attack(unit, targets):
                # Opposing team is all dead and unit isn't last to be processed
                if all(unit["hp"] <= 0 for unit in targets) and unit is not units[-1]:
                    # Completed before round finished
                    current_round -= 1
                    break
            else:
                if move(unit, targets):
                    if attack(unit, targets):
                        # Opposing team is all dead and unit isn't last to be processed
                        if all(unit["hp"] <= 0 for unit in targets) and unit is not units[-1]:
                            # Completed before round finished
                            current_round -= 1
                            break
        goblins = list(filter(lambda x: x["hp"] > 0, goblins))
        elfs = list(filter(lambda x: x["hp"] > 0, elfs))

        # print(current_round)
        # draw(world, goblins + elfs)

    winning_team = elfs
    winning_team_str = "elfs"
    if len(elfs) == 0:
        winning_team = goblins
        winning_team_str = "goblins"
    sum_hp = sum(unit["hp"] for unit in winning_team if unit["hp"] > 0)
    outcome = current_round * sum_hp
    # print(f"{outcome} = ({sum_hp} x {current_round})")
    return outcome, winning_team_str, len(winning_team)


def day15(submit_answer=False):
    data = get_data(day=15, year=2018).split("\n")

    world = collections.defaultdict(lambda: "#")

    goblins = []
    elfs = []

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "G" or char == "E":
                world[(x, y)] = "."
                unit = {"pos": (x, y), "hp": 200, "attack_power": 3, "type": char}
                if char == "G":
                    goblins.append(unit)
                else:
                    elfs.append(unit)
            else:
                world[(x, y)] = char

    outcome, __, __ = simulate(world, copy.deepcopy(goblins), copy.deepcopy(elfs))

    def find_min_boost(range):
        for i in range:
            new_goblins = copy.deepcopy(goblins)
            new_elfs = copy.deepcopy(elfs)
            for unit in new_elfs:
                unit["attack_power"] += i
            outcome, winning_team, num_units = simulate(world, new_goblins, new_elfs)
            if winning_team == "elfs" and num_units == len(elfs):
                return i, outcome
    boost, answer2 = find_min_boost(range(1, 200, 10))
    boost, answer2 = find_min_boost(range(boost, 0, -2))
    boost, answer2 = find_min_boost(range(boost, 200, 1))

    if submit_answer:
        submit(outcome, 1, day=22, year=2018)
        submit(answer2, 2, day=22, year=2018)
    return outcome, answer2
