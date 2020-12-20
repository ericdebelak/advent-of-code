from itertools import count


def test_task_one():
    assert task_one('test-data.txt') == 295
    assert task_one('real-data.txt') == 2382


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


def test_task_two():
    assert task_two('test-data.txt') == 1068781
    assert task_two('real-data.txt') == 906332393333683


def task_two(filename):
    earliest_time, bus_schedule = [line.strip('\n') for line in open(filename)]
    buses = {
        int(bus): offset
        for offset, bus in enumerate(bus_schedule.split(','))
        if bus != 'x'
    }
    buses = sorted(buses.items(), reverse=True)  # start with our biggest values to go through fewer iterations
    start, step = 0, 1
    for bus, offset in buses:
        for time in count(start, step):  # go through our times until we find a factor
            if (time + offset) % bus == 0:  # found a factor
                start = time  # reset our start time for the next bus at our current time
                step *= bus  # set our steps to remain a factor for all previous buses
                break
    return time
