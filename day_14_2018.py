from aocd import get_data, submit


def day14(submit_answer=False):
    data = get_data(day=14, year=2018)

    scores = [3, 7]

    first_elf = 0
    second_elf = 1

    target_score_seq = list(map(int, data))

    while scores[-6:] != target_score_seq:
        current_first_elf = scores[first_elf]
        current_second_elf = scores[second_elf]
        for new_score in map(int, str(current_first_elf + current_second_elf)):
            scores.append(new_score)
            if scores[-6:] == target_score_seq:
                break
        first_elf = (first_elf + 1 + current_first_elf) % len(scores)
        second_elf = (second_elf + 1 + current_second_elf) % len(scores)

    data_index = len(scores) - 6
    answer1 = "".join(map(str, scores[int(data):int(data)+10]))

    if submit_answer:
        submit(answer1, 1, day=14, year=2018)
        submit(data_index, 2, day=14, year=2018)
    return answer1, data_index
