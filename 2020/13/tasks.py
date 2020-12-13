from functools import reduce


def test_task_one():
    assert 295 == task_one('test-data.txt')
    assert 2382 == task_one('real-data.txt')


def task_one(filename):
    earliest_time, bus_schedule = [line.strip('\n') for line in open(filename)]
    earliest_time = int(earliest_time)
    buses = [int(bus) for bus in bus_schedule.split(',') if bus != 'x']
    next_bus = best_time = False
    for bus in buses:
        time = 0
        while time < earliest_time:
            time += bus
        if time < best_time or not best_time:
            best_time = time
            next_bus = bus
    return (best_time - earliest_time) * next_bus


def chinese_remainder(n, a):
    # from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python, but modified to use pow
    total = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        total += a_i * pow(p, -1, n_i) * p
    return total % prod


def test_task_two():
    assert 1068781 == task_two('test-data.txt')
    assert 906332393333683 == task_two('real-data.txt')


def task_two(filename):
    earliest_time, bus_schedule = [line.strip('\n') for line in open(filename)]
    buses = bus_schedule.split(',')
    divisors = []
    remainders = []
    for index in range(len(buses)):
        if buses[index] != "x":
            divisors.append(int(buses[index]))
            remainders.append(int(buses[index]) - index)
    return chinese_remainder(divisors, remainders)




