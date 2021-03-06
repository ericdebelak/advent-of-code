def test_task_one():
    assert task_one('test-data-one.txt') == 7 * 5
    assert task_one('test-data-two.txt') == 22 * 10
    assert task_one('real-data.txt') == 2070


def task_one(filename):
    lines = [int(line) for line in open(filename)]
    lines.sort()
    count_of_one = 0
    # our device always has a difference of three, so we'll start with a count of 1
    count_of_three = 1
    for index, current_number in enumerate(lines):
        previous_number = 0 if index == 0 else lines[index - 1]
        diff = current_number - previous_number
        if diff == 1:
            count_of_one += 1
        elif diff == 3:
            count_of_three += 1
    return count_of_one * count_of_three


def test_build_graph():
    assert _build_graph([0, 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, 22]) == {
        0: [1],
        1: [4],
        4: [5, 6, 7],
        5: [6, 7],
        6: [7],
        7: [10],
        10: [11, 12],
        11: [12],
        12: [15],
        15: [16],
        16: [19],
        19: [22],
        22: []
    }


def _build_graph(adapters):
    # get a list of all potential children adapters (+1, 2 or 3) if they are in our adapters list
    return {adapter: [adapter + x for x in [1, 2, 3] if adapter + x in adapters] for adapter in adapters}


def test_count_paths():
    graph = {
        0: [1],
        1: [4],
        4: [5, 6, 7],
        5: [6, 7],
        6: [7],
        7: [10],
        10: [11, 12],
        11: [12],
        12: [15],
        15: [16],
        16: [19],
        19: [22],
        22: []
    }
    assert _count_paths(graph) == {
        0: 1,
        1: 1,
        4: 1,
        5: 1,
        6: 2,   # 6 can be reached from 5 (+1) or 4 (+1)
        7: 4,   # 7 can be reached from 6 (+2), 5 (+1) or 4 (+1)
        10: 4,
        11: 4,
        12: 8,  # 12 can be reached from 11 (+4) or 10 (+4)
        15: 8,
        16: 8,
        19: 8,
        22: 8
    }


# for each adapter, count how many possible paths to reach it
def _count_paths(graph):
    # we have one path to get to 0, so that is how we initialize our variable
    # key is the adapter number and value is the number of paths
    paths = {0: 1}
    for parent, children in graph.items():
        for child in children:
            # for every time the child appears in the path
            # we add all possible paths of its parent
            paths[child] = sum([paths.get(child, 0), paths[parent]])
    return paths


def test_task_two():
    assert task_two('test-data-one.txt') == 8
    assert task_two('test-data-two.txt') == 19208
    assert task_two('real-data.txt') == 24179327893504


def task_two(filename):
    lines = [int(line) for line in open(filename)]
    lines.sort()
    # create a final number, 3 higher than the last line
    final = max(lines) + 3
    # create a list of all adapters, including 0 for start and the final number
    adapters = [0] + lines + [final]
    graph = _build_graph(adapters)
    paths = _count_paths(graph)
    return paths[final]
