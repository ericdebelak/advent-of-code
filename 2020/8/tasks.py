from copy import deepcopy


def test_task_one():
    assert task_one('test-data.txt') == 5
    assert task_one('real-data.txt') == 1753


def task_one(filename):
    lines = [line.strip('\n') for line in open(filename)]
    line_count = dict.fromkeys(range(len(lines)), 0)
    position = acc_value = 0
    # keep executing until the program repeats (line count > 0)
    while line_count[position] == 0:
        line_count[position] += 1
        position, acc_value = _execute_line(position, acc_value, lines)
    return acc_value


def test_execute_line():
    assert _execute_line(0, 0, ['nop +0']) ==  (1, 0)
    assert _execute_line(0, 0, ['jmp +3']) ==  (3, 0)
    assert _execute_line(0, 0, ['acc +5']) ==  (1, 5)


def _execute_line(position, acc_value, lines):
    action, value = lines[position].split()
    position = eval(f'position {value}') if action == 'jmp' else position + 1
    acc_value = eval(f'acc_value {value}') if action == 'acc' else acc_value
    return position, acc_value


def test_correct_corrupted_line():
    assert _correct_corrupted_line('jmp +3') == 'nop +3'
    assert _correct_corrupted_line('nop -3') == 'jmp -3'


def _correct_corrupted_line(line):
    corrections = {
        'jmp': 'nop',
        'nop': 'jmp'
    }
    for key, value in corrections.items():
        if key in line:
            return line.replace(key, value)
    return line


def _line_is_valid(lines):
    position = acc_value = 0
    line_count = dict.fromkeys(range(len(lines)), 0)
    # execute until we hit the end or it repeats (line count > 0)
    while position < len(lines) and line_count[position] == 0:
        line_count[position] += 1
        position, acc_value = _execute_line(position, acc_value, lines)
    # if we hit the end, return the value
    return acc_value if position == len(lines) else False


def test_task_two():
    assert task_two('test-data.txt') == 8
    assert task_two('real-data.txt') == 733


def task_two(filename):
    lines = [line.strip('\n') for line in open(filename)]
    for index in range(len(lines)):
        new_lines = deepcopy(lines)
        new_lines[index] = _correct_corrupted_line(new_lines[index])
        result = _line_is_valid(new_lines)
        if result:
            return result
    return False

