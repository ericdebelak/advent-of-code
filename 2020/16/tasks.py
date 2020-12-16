from copy import deepcopy


def test_task_one():
    assert 71 == task_one('test-data.txt')
    assert 24110 == task_one('real-data.txt')


def task_one(filename):
    with open(filename, 'r') as file:
        rules, my_ticket, other_tickets = file.read().split('\n\n')
        valid_numbers = _build_valid_numbers(rules)
        invalid_numbers = _find_invalid_numbers(valid_numbers, other_tickets)
    return sum(invalid_numbers)


def test_build_valid_numbers():
    assert [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 33, 34] == _build_valid_numbers('class: 1-3 or 5-7\nrow: 6-11 or 33-34')


def _build_valid_numbers(text):
    valid_numbers = []
    lines = text.splitlines()
    for line in lines:
        valid_numbers = _get_valid_numbers_from_lines(line, valid_numbers)
    return valid_numbers


def _get_valid_numbers_from_lines(line, valid_numbers):
    key, values = line.split(': ')
    groups = values.split(' or ')
    for group in groups:
        first, second = [int(x) for x in group.split('-')]
        for number in range(first, second + 1):
            if number not in valid_numbers:
                valid_numbers.append(number)
    return valid_numbers


def test_find_invalid_numbers():
    assert [7, 47] == _find_invalid_numbers([1, 2, 3], 'nearby tickets:\n7,3,47')


def _find_invalid_numbers(valid_numbers, text):
    invalid_numbers = []
    lines = text.splitlines()
    for line in lines[1:]:
        numbers = [int(x) for x in line.split(',')]
        for number in numbers:
            if number not in valid_numbers:
                invalid_numbers.append(number)
    return invalid_numbers


def test_remove_invalid_tickets():
    assert [[1, 6, 3], [7, 5, 1]] == _remove_invalid_tickets(
        [1, 2, 3, 4, 5, 6, 7],
        'nearby tickets:\n1,6,3\n7,3,47\n7,5,1'
    )


def _remove_invalid_tickets(valid_numbers, text):
    valid_tickets = []
    lines = text.splitlines()
    for ticket in lines[1:]:
        numbers = [int(x) for x in ticket.split(',')]
        if all(number in valid_numbers for number in numbers):
            valid_tickets.append(numbers)
    return valid_tickets


def test_build_index_graph():
    assert {
        0: [6, 8],
        1: [45, 78]
    } == _build_index_graph([[6, 45], [8, 78]])


def _build_index_graph(tickets):
    graph = {}
    for ticket in tickets:
        for index, value in enumerate(ticket):
            if graph.get(index):
                graph[index].append(value)
            else:
                graph[index] = [value]
    return graph


def test_check_if_rule_works():
    assert _check_if_rule_works('row: 0-5 or 8-19', [3, 15, 5])
    assert not _check_if_rule_works('seat: 0-13 or 16-19', [3, 15, 5])


def _check_if_rule_works(rule, numbers):
    valid_numbers = _get_valid_numbers_from_lines(rule, [])
    return all(number in valid_numbers for number in numbers)


def _build_rule_columns_graph(rules, column_graph):
    rule_columns = {}  # build which columns can satisfy which rules
    for rule_index, rule in enumerate(rules.splitlines()):
        for index, numbers in column_graph.items():
            if _check_if_rule_works(rule, numbers):
                if rule_columns.get(rule_index):
                    rule_columns[rule_index].append(index)
                else:
                    rule_columns[rule_index] = [index]
    return rule_columns


def _find_next_number_to_remove(rule_columns, removed_numbers):
    for index, numbers in rule_columns.items():
        if len(numbers) == 1 and numbers[0] not in removed_numbers:
            number_to_remove = numbers[0]
            removed_numbers.append(number_to_remove)
            return False, number_to_remove, removed_numbers
    return True, False, removed_numbers


def _simplify_rule_columns(rule_columns):
    simplified = False
    removed_numbers = []
    while not simplified:
        simplified, number_to_remove, removed_numbers = _find_next_number_to_remove(rule_columns, removed_numbers)
        if number_to_remove is not False:
            new_rule_columns = deepcopy(rule_columns)
            for index, numbers in new_rule_columns.items():
                if number_to_remove in numbers and len(numbers) > 1:
                    numbers.remove(number_to_remove)
            rule_columns = new_rule_columns
    return rule_columns


def test_task_two():
    assert 6766503490793 == task_two('real-data.txt')


def task_two(filename):
    with open(filename, 'r') as file:
        rules, my_ticket, other_tickets = file.read().split('\n\n')
        my_ticket = [int(x) for x in my_ticket.splitlines()[1].split(',')]
        valid_numbers = _build_valid_numbers(rules)
        valid_tickets = _remove_invalid_tickets(valid_numbers, other_tickets)
        column_graph = _build_index_graph(valid_tickets)  # build a graph of all values from each column
        rule_columns = _build_rule_columns_graph(rules, column_graph)  # which rules can be satisfied with which columns
        simplified_rule_columns = _simplify_rule_columns(rule_columns)  # simplify until 1 column is satisfied per rule
        departure_rule_indexes = [index for index, rule in enumerate(rules.splitlines()) if 'departure' in rule]
        total = 1
        for index in departure_rule_indexes:
            total *= my_ticket[simplified_rule_columns[index][0]]
    return total
