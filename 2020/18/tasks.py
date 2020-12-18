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
    total = 0
    current_index = 0
    while current_index + 1 < len(line):
        item = _get_item(line[current_index])
        if _is_int(item) and current_index < 3:
            third_item = _get_item(line[current_index+2])
            total = eval(f'{item}{line[current_index + 1]}{third_item}')
            current_index += 3
        elif not _is_int(item) and current_index >= 3:
            next_item = _get_item(line[current_index + 1])
            total = eval(f'{total}{line[current_index]}{next_item}')
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
    assert 122 == task_one('test-data.txt')
    assert 1402255785165 == task_one('real-data.txt')


def task_one(filename):
    total = 0
    lines = [line.strip('\n') for line in open(filename)]
    for line in lines:
        total += _evaluate_line(_break_into_groups(line))
    return total


