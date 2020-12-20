import re


def _bag_check(lines, bags_that_work):
    has_changed = False
    for parent_bag, children_bags in [line.split('s contain ') for line in lines]:
        for bag in bags_that_work:
            if bag in children_bags and parent_bag not in bags_that_work:
                bags_that_work.append(parent_bag)
                has_changed = True
    return has_changed, bags_that_work


def test_task_one():
    assert task_one('test-data.txt') == 4
    assert task_one('real-data.txt') == 169


def task_one(filename):
    lines = [line.strip('\n') for line in open(filename)]
    bag_search = 'shiny gold bag'
    bags_that_work = [bag_search]
    has_changed = True
    while has_changed:
        has_changed, bags_that_work = _bag_check(lines, bags_that_work)
    # remove our original bag
    bags_that_work.remove(bag_search)
    return len(bags_that_work)


def test_get_children_bags_with_count():
    assert _get_children_bags_with_count(
        '3 dotted magenta bags, 2 shiny beige bags, 3 plaid brown bags, 5 clear indigo bags.'
    ) == (13, {
        'clear indigo bag': 5,
        'dotted magenta bag': 3,
        'plaid brown bag': 3,
        'shiny beige bag': 2,
    })


def _get_children_bags_with_count(bag_string):
    total_count = 0
    result = {}
    if bag_string != 'no other bags.':
        for bag in bag_string.split(', '):
            count, bag_name = re.findall(r'(\d|[a-z]+\s[a-z]+\sbag)', bag)
            result[bag_name] = int(count)
            total_count += int(count)
    return total_count, result


def test_build_graph():
    text = '''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.'''
    lines = text.splitlines()
    assert _build_graph(lines) == {
        'dark orange bag': {
            'children': {
                'bright white bag': 3,
                'muted yellow bag': 4
            },
            'count': 7
        },
        'light red bag': {
            'children': {
                'bright white bag': 1,
                'muted yellow bag': 2
            },
            'count': 3
        }
    }


def _build_graph(lines):
    bag_graph = {}
    for parent_bag, children_bags in [line.split('s contain ') for line in lines]:
        bag_graph[parent_bag] = {
            'count': (_get_children_bags_with_count(children_bags))[0],
            'children': (_get_children_bags_with_count(children_bags))[1]
        }
    return bag_graph


def _get_total_recursive(bag_graph, parent_name, child_name, total=0, modifier=1):
    if child_name in bag_graph[parent_name]['children']:
        # our modifier is cumulative since 2 bags of 2 bags of 2 bags is 8 of the last bag
        modifier = modifier * bag_graph[parent_name]['children'][child_name]
    total += modifier * bag_graph[child_name]['count']
    for grand_child_name in bag_graph[child_name]['children']:
        total = _get_total_recursive(bag_graph, child_name, grand_child_name, total, modifier)
    return total


def test_task_two():
    assert task_two('test-data.txt') == 32
    assert task_two('test-data-two.txt') == 126
    assert task_two('real-data.txt') == 82372


def task_two(filename):
    lines = [line.strip('\n') for line in open(filename)]
    bag_graph = _build_graph(lines)
    bag_search = 'shiny gold bag'
    return _get_total_recursive(bag_graph, bag_search, bag_search)
