def test_task_one():
    assert 436 == task_one([0, 3, 6])
    assert 1 == task_one([1, 3, 2])
    assert 10 == task_one([2, 1, 3])
    assert 27 == task_one([1, 2, 3])
    assert 78 == task_one([2, 3, 1])
    assert 438 == task_one([3, 2, 1])
    assert 1836 == task_one([3, 1, 2])
    assert 1428 == task_one([2, 0, 6, 12, 1, 3])  # my puzzle input


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
    assert 175594 == task_one([0, 3, 6], 30000000)
    assert 3718541 == task_one([2, 0, 6, 12, 1, 3], 30000000)  # my puzzle input
