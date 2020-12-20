from copy import copy


def test_task_one():
    assert task_one('test-data.txt', 5) == 127
    assert task_one('real-data.txt', 25) == 248131121


def task_one(filename, preamble):
    lines = [int(line) for line in open(filename)]
    for index in range(preamble, len(lines)):
        # get previous lines
        previous_lines = [int(x) for x in lines[index - preamble:index]]
        result = _check_for_match(previous_lines, lines[index])
        if not result:
            return lines[index]
    return False


def test_check_for_match_with_match():
    lines = [35, 20, 15, 25, 47]
    assert _check_for_match(lines, 40) == 40


def test_check_for_match_no_match():
    lines = [95, 102, 117, 150, 182]
    assert not _check_for_match(lines, 127)


def _check_for_match(lines, match):
    for line_one in lines:
        for line_two in lines:
            if line_one != line_two and line_one + line_two == match:
                return match
    return False


def test_check_for_low_high():
    lines = [35, 20, 15, 25, 47, 40, 62]
    assert _check_for_low_high(lines, 127) == 62


def _check_for_low_high(lines, match):
    total = 0
    lowest_number = highest_number = lines[0]
    for line in lines:
        highest_number = line if highest_number < line else highest_number
        lowest_number = line if lowest_number > line else lowest_number
        total += line
        if total == match:
            return lowest_number + highest_number
        if total > match:
            # if we've gone over, we need to start again starting with the second line
            new_lines = copy(lines)
            new_lines.pop(0)
            return _check_for_low_high(new_lines, match)


def test_task_two():
    assert task_two('test-data.txt', 5) == 62
    assert task_two('real-data.txt', 25) == 31580383


def task_two(filename, preamble):
    invalid_number = task_one(filename, preamble)
    lines = [int(line) for line in open(filename)]
    return _check_for_low_high(lines, invalid_number)
