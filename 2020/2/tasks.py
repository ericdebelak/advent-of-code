def _parse_line(line):
    numbers, char, password = line.split()
    low, high = numbers.split('-')
    return int(low), int(high), char.strip(':'), password


def test_task_one():
    assert 2 == task_one('test-data.txt')
    assert 564 == task_one('real-data.txt')


def task_one(filename):
    num_valid = 0
    for low, high, char, password in [_parse_line(line) for line in open(filename)]:
        count = password.count(char)
        if low <= count <= high:
            num_valid += 1
    return num_valid


def test_task_two():
    assert 1 == task_two('test-data.txt')
    assert 325 == task_two('real-data.txt')


def task_two(filename):
    num_valid = 0
    for low, high, char, password in [_parse_line(line) for line in open(filename)]:
        at_low = _char_at_position(password, char, low - 1)
        at_high = _char_at_position(password, char, high - 1)
        if not (at_low and at_high) and (at_low or at_high):
            num_valid += 1
    return num_valid


def _char_at_position(string, char, position):
    return string[position] == char
