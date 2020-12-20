def _parse_line(line):
    numbers, char, password = line.split()
    low, high = numbers.split('-')
    return int(low), int(high), char.strip(':'), password


def test_task_one():
    assert task_one('test-data.txt') == 2
    assert task_one('real-data.txt') == 564


def task_one(filename):
    num_valid = 0
    for low, high, char, password in [_parse_line(line) for line in open(filename)]:
        count = password.count(char)
        if low <= count <= high:
            num_valid += 1
    return num_valid


def test_task_two():
    assert task_two('test-data.txt') == 1
    assert task_two('real-data.txt') == 325


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
