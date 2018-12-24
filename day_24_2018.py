from aocd import get_data, submit
import itertools

import copy
import re


def calc_damage(attacker, victim):
    damage = attacker["damage"] * attacker["units"]
    if attacker["damage_type"] in victim["weakness"]:
        damage *= 2
    elif attacker["damage_type"] in victim["immunity"]:
        damage = 0
    return damage


def simulate(groups):
    while True:
        # Target Selection
        # Sort by effective power and then initiative in decreasing order (100, 50, etc.)
        groups = sorted(groups, key=lambda x: (x["units"] * x["damage"], x["initiative"]))[::-1]
        chosen_targets = []
        for group in groups:
            if group["units"] <= 0:  # Dead group
                continue
            target = "infection"
            if group["type"] == "infection":
                target = "immune"
            targets = filter(lambda x: x not in chosen_targets and x["type"] == target, groups)
            targets = sorted(targets, key=lambda x: (calc_damage(group, x), x["units"] * x["damage"], x["initiative"]))[::-1]
            if len(targets) > 0:
                chosen_target = targets[0]
                if calc_damage(group, chosen_target) > 0:
                    group["chosen_target"] = chosen_target
                    chosen_targets.append(chosen_target)
        # Attacking
        groups = sorted(groups, key=lambda x: x["initiative"])[::-1]
        total_units_killed = 0
        for group in groups:
            if group["units"] <= 0:  # Dead group
                continue
            if "chosen_target" in group:
                chosen_target = group["chosen_target"]
                units_killed = calc_damage(group, chosen_target) // chosen_target["hp"]
                chosen_target["units"] -= units_killed
                total_units_killed += units_killed
                del group["chosen_target"]

        groups = list(filter(lambda x: x["units"] > 0, groups))

        immune_system = list(filter(lambda x: x["type"] == "immune", groups))
        infection = list(filter(lambda x: x["type"] == "infection", groups))
        if len(immune_system) == 0:
            winning_army_units = sum(group["units"] for group in infection)
            return "infection", winning_army_units
        if len(infection) == 0:
            winning_army_units = sum(group["units"] for group in immune_system)
            return "immune", winning_army_units
        if total_units_killed == 0:
            return "stalemate", 0


def day24(submit_answer=False):
    data = get_data(day=24, year=2018).split("\n")
    groups = []

    def process(line, type):
        units, hp, damage, initiative = map(int, re.findall("(\\d+)", line))
        immunity_weakness = re.findall("\\((.+)\\)", line)
        damage_type = re.findall("does\\s\\d+\\s(.+)\\sdamage", line)[0]
        immunity = []
        weakness = []
        if immunity_weakness:
            immunity_weakness = immunity_weakness[0].split(";")
            for x in immunity_weakness:
                if "weak" in x:
                    weakness.extend(map(str.strip, x.split(" to ")[1].split(",")))
                if "immune" in x:
                    immunity.extend(map(str.strip, x.split(" to ")[1].split(",")))
        return {"type": type, "units": units, "hp": hp, "immunity": immunity, "weakness": weakness, "damage": damage,
                "damage_type": damage_type, "initiative": initiative}

    infection_line = 0
    for i, line in enumerate(data[1:]):
        if line == "":
            infection_line = i + 3
            break
        groups.append(process(line, "immune"))

    for line in data[infection_line:]:
        groups.append(process(line, "infection"))

    __, answer1 = simulate(copy.deepcopy(groups))

    def find_min_boost(start, step):
        for i in range(start, 1000, step):
            new_groups = copy.deepcopy(groups)
            for group in new_groups:
                if group["type"] == "immune":
                    group["damage"] += i
            winning_side, units = simulate(new_groups)
            if winning_side == "immune":
                return i, units
    boost, answer2 = find_min_boost(15, 15)
    boost, answer2 = find_min_boost(boost - 15, 1)

    if submit_answer:
        submit(answer1, 1, day=24, year=2018)
        submit(answer2, 2, day=24, year=2018)
    return answer1, answer2
