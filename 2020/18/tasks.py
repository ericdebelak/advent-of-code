from copy import copy


def test_break_into_groups():
    assert ['1', '+', ['2', '*', '3'],  '+', ['4',  '*',  ['5', '+', '6']]] == _break_into_groups(
        '1 + (2 * 3) + (4 * (5 + 6))'
    )


def _break_into_groups(line):
    line = line.replace(' ', '')
    groups = []
    open_paren = []
    close_paren = []
    for index, char in enumerate(line):
        if char == '(':
            open_paren.append(index)
        elif char == ')':
            close_paren.append(index)
            if len(open_paren) == len(close_paren):
                groups.append(_break_into_groups(line[open_paren[0]+1:index]))
                open_paren = []
                close_paren = []
        elif len(open_paren) == 0:
            groups.append(char)
    return groups


def test_evaluate_line():
    assert 51 == _evaluate_line(['1', '+', ['2', '*', '3'],  '+', ['4',  '*',  ['5', '+', '6']]])
    assert 10088 == _evaluate_line([['3', '*', ['4', '*', '8'], '*', '5', '*', '7', '*', '3'], '+', '8'])


def _evaluate_line(line):
    total = _get_item(line[0])  # init to first item
    current_index = 1  # since we have the first item, start at index 1
    while current_index + 1 < len(line):
        item = _get_item(line[current_index])
        if not _is_int(item):  # only do operations if we don't have an int
            next_item = _get_item(line[current_index + 1])
            total = eval(f'{total}{item}{next_item}')
            current_index += 2
        else:
            current_index += 1
    return total


def _get_item(item):
    if isinstance(item, list):
        item = _evaluate_line(item)
    return item


def _is_int(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


def test_task_one():
    assert task_one('test-data.txt') == 122
    assert task_one('real-data.txt') == 1402255785165


def task_one(filename):
    total = 0
    lines = [line.strip('\n') for line in open(filename)]
    for line in lines:
        total += _evaluate_line(_break_into_groups(line))
    return total


def test_add_then_multiply():
    assert _add_then_multiply(['1', '+', '2', '*', '3']) == 9
    assert _add_then_multiply(['1', '+', '2', '*', '3', '*', '3', '+', '1']) == 36
    assert _add_then_multiply(['1', '+', ['2', '*', '3'], '*', '3', '+', '1']) == 28


def _add_then_multiply(line):
    new_line = copy(line)
    for index, char in enumerate(line):
        if char == '+' or (char == '*' and '+' not in line):
            first = _get_item_only_add(line[index - 1])
            second = _get_item_only_add(line[index + 1])
            new_line = line[0:index - 1] + [eval(f'{first}{char}{second}')] + line[index + 2:]
            return _add_then_multiply(new_line)
    return int(new_line[0])


def _get_item_only_add(item):
    if isinstance(item, list):
        item = _add_then_multiply(item)
    return item


def test_task_two():
    assert task_two('real-data.txt') == 119224703255966


def task_two(filename):
    total = 0
    lines = [line.strip('\n') for line in open(filename)]
    for line in lines:
        total += _add_then_multiply(_break_into_groups(line))
    return total
