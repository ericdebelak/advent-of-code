def test_task_one():
    assert task_one('test-data.txt') == 514579
    assert task_one('real-data.txt') == 1014624


def task_one(filename):
    lines = [int(x) for x in open(filename)]
    for first in lines:
        for second in lines:
            if first + second == 2020:
                return first * second


def test_task_two():
    assert task_two('test-data.txt') == 241861950
    assert task_two('real-data.txt') == 80072256


def task_two(filename):
    lines = [int(x) for x in open(filename)]
    for first in lines:
        for second in lines:
            for third in lines:
                if first + second + third == 2020:
                    return first * second * third
