from aocd import get_data, submit

import collections


def day20(submit_answer=False):
    data = get_data(day=20, year=2018)
    data = collections.deque(data[1:-1])

    root = []

    def process(data):
        node = {"branches": [[]]}
        while len(data) > 0:
            char = data.popleft()
            if char == ")":
                return node
            elif char == "|":
                node["branches"].append([])
            elif char == "(":
                node["branches"][-1].append(process(data))
            else:
                node["branches"][-1].append(char)

    while len(data) > 0:
        char = data.popleft()
        if char == "(":
            root.append(process(data))
        else:
            root.append(char)

    world = collections.defaultdict(lambda: "#")
    offset = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
    walls = {"N": "-", "E": "|", "S": "-", "W": "|"}
    
    def generate_world(current_node, current_paths=None):
        if current_paths is None:
            current_paths = {(0, 0)}
        for node in current_node:
            if isinstance(node, str):
                x_off, y_off = offset[node]
                new_poses = set()
                for (x, y) in current_paths:
                    x += x_off
                    y += y_off
                    world[(2 * x, 2 * y)] = "."
                    world[(2 * x - x_off, 2 * y - y_off)] = walls[node]
                    new_poses.add((x, y))
                current_paths = new_poses
            else:
                new_branches = set()
                for branch in node["branches"]:
                    new_branches |= generate_world(branch, current_paths)
                current_paths = new_branches

        return current_paths
    generate_world(root)

    costs = collections.defaultdict(lambda: 10000)

    open = [(0, 0, 0)]
    while len(open) > 0:
        x, y, current_cost = open.pop()
        costs[(x, y)] = current_cost
        surroundings = [((x + x_off, y + y_off), (2 * x + x_off, 2 * y + y_off)) for x_off, y_off in offset.values()]
        surroundings = [((r_x, r_y), world[(w_x, w_y)] in walls.values()) for (r_x, r_y), (w_x, w_y) in surroundings]
        for pos, is_open in surroundings:
            if is_open:
                if pos in costs and (current_cost + 1) >= costs[pos]:
                    continue
                open.append((*pos, current_cost + 1))

    max_distance = max(costs.values())
    answer2 = sum(1 for cost in costs.values() if cost >= 1000)
    if submit_answer:
        submit(max_distance, 1, day=20, year=2018)
        submit(answer2, 2, day=20, year=2018)
    return max_distance, answer2
