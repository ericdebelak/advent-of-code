def test_task_one():
    assert 514579 == task_one('test-data.txt')
    assert 1014624 == task_one('real-data.txt')


def task_one(filename):
    lines = [int(x) for x in open(filename)]
    for first in lines:
        for second in lines:
            if first + second == 2020:
                return first * second


def test_task_two():
    assert 241861950 == task_two('test-data.txt')
    assert 80072256 == task_two('real-data.txt')


def task_two(filename):
    lines = [int(x) for x in open(filename)]
    for first in lines:
        for second in lines:
            for third in lines:
                if first + second + third == 2020:
                    return first * second * third
