from aocd import get_data, submit
import copy


def day13(submit_answer=False):
    data = get_data(day=13, year=2018).split("\n")

    init_carts = {}
    cart_dir = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}
    left_cart_dir = {"^": "<", "v": ">", "<": "v", ">": "^"}
    straight_cart_dir = {"^": "^", "v": "v", "<": "<", ">": ">"}
    right_cart_dir = {"^": ">", "v": "<", "<": "^", ">": "v"}
    intersection_turn = [left_cart_dir, straight_cart_dir, right_cart_dir]

    for y, line in enumerate(data):
        if "^" in line or "v" in line or "<" in line or ">" in line:
            for x, char in enumerate(line):
                if char in cart_dir.keys():
                    init_carts[(x, y)] = {"direction": char, "turn_count": 0}

    crash = None
    carts = copy.deepcopy(init_carts)
    while crash is None:
        for x, y in sorted(carts.keys(), key=lambda x: (x[1], x[0])):
            cart = carts.pop((x, y))
            offset_x, offset_y = cart_dir[cart["direction"]]
            path_infront = data[y + offset_y][x + offset_x]
            if (x + offset_x, y + offset_y) in carts:
                crash = (x + offset_x, y + offset_y)
                break
            carts[(x + offset_x, y + offset_y)] = cart

            if path_infront == "/":
                if cart["direction"] == "<" or cart["direction"] == ">":
                    cart["direction"] = left_cart_dir[cart["direction"]]
                else:
                    cart["direction"] = right_cart_dir[cart["direction"]]
            elif path_infront == "\\":
                if cart["direction"] == "<" or cart["direction"] == ">":
                    cart["direction"] = right_cart_dir[cart["direction"]]
                else:
                    cart["direction"] = left_cart_dir[cart["direction"]]
            elif path_infront == "+":
                cart["direction"] = intersection_turn[cart["turn_count"]][cart["direction"]]
                cart["turn_count"] = (cart["turn_count"] + 1) % 3

    carts = copy.deepcopy(init_carts)

    while len(carts) > 1:
        for x, y in sorted(carts.keys(), key=lambda a: (a[1], a[0])):
            if (x, y) not in carts:
                continue
            cart = carts.pop((x, y))
            offset_x, offset_y = cart_dir[cart["direction"]]
            path_infront = data[y + offset_y][x + offset_x]
            if (x + offset_x, y + offset_y) in carts:
                carts.pop((x + offset_x, y + offset_y))
                continue
            carts[(x + offset_x, y + offset_y)] = cart

            if path_infront == "/":
                if cart["direction"] == "<" or cart["direction"] == ">":
                    cart["direction"] = left_cart_dir[cart["direction"]]
                else:
                    cart["direction"] = right_cart_dir[cart["direction"]]
            elif path_infront == "\\":
                if cart["direction"] == "<" or cart["direction"] == ">":
                    cart["direction"] = right_cart_dir[cart["direction"]]
                else:
                    cart["direction"] = left_cart_dir[cart["direction"]]
            elif path_infront == "+":
                cart["direction"] = intersection_turn[cart["turn_count"]][cart["direction"]]
                cart["turn_count"] = (cart["turn_count"] + 1) % 3

    last_cart_pos = next(iter(carts.keys()))

    answer1 = f"{crash[0]},{crash[1]}"
    answer2 = f"{last_cart_pos[0]},{last_cart_pos[1]}"

    if submit_answer:
        submit(answer1, 1, day=13, year=2018)
        submit(answer2, 2, day=13, year=2018)
    return answer1, answer2
