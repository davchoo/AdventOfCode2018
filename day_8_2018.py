from aocd import get_data, submit


def day8(submit_answer=False):
    data = get_data(day=8, year=2018).split()

    data = list(map(int, data))

    parents = [{"num_children": data.pop(0), "num_metadata": data.pop(0), "children": []}]

    sum_metadata = 0

    while len(data) > 0:
        if len(parents[0]["children"]) < parents[0]["num_children"]:
            parents.insert(0, {"num_children": data.pop(0), "num_metadata": data.pop(0), "children": []})
        else:
            parents[0]["metadata"] = [data.pop(0) for i in range(parents[0]["num_metadata"])]
            sum_metadata += sum(parents[0]["metadata"])
            if len(parents) == 1:
                parents = parents[0]
                break
            parents[1]["children"].append(parents.pop(0))

    def get_value(node):
        value = 0
        if len(node["children"]) > 0:
            for index in node["metadata"]:
                index -= 1
                if 0 <= index < len(node["children"]):
                    value += get_value(node["children"][index])
        else:
            value = sum(node["metadata"])
        return value

    root_value = get_value(parents)

    if submit_answer:
        submit(sum_metadata, 1, day=8, year=2018)
        submit(root_value, 2, day=8, year=2018)
    return sum_metadata, root_value
