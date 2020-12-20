def test_task_one():
    assert task_one([0, 3, 6]) == 436
    assert task_one([1, 3, 2]) == 1
    assert task_one([2, 1, 3]) == 10
    assert task_one([1, 2, 3]) == 27
    assert task_one([2, 3, 1]) == 78
    assert task_one([3, 2, 1]) == 438
    assert task_one([3, 1, 2]) == 1836
    assert task_one([2, 0, 6, 12, 1, 3]) == 1428  # my puzzle input


def task_one(starting_numbers, end=2020):
    # number, last time called
    turn_graph = {
        number: index
        for index, number in enumerate(starting_numbers[:-1])
    }
    next_number = starting_numbers[-1]
    for turn in range(len(starting_numbers[:-1]), end):
        previous_number = next_number
        # first time
        if previous_number not in turn_graph:
            next_number = 0
        else:
            # difference between this appearance and the last one
            next_number = turn - turn_graph[previous_number]
        turn_graph[previous_number] = turn
    return previous_number


def test_task_two():
    assert task_one([0, 3, 6], 30000000) == 175594
    assert task_one([2, 0, 6, 12, 1, 3], 30000000) == 3718541  # my puzzle input
