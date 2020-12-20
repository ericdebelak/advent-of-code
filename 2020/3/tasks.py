def test_task_one():
    assert task_one('test-data.txt') == 7
    assert task_one('real-data.txt') == 228


def task_one(filename):
    position = num_trees = 0
    for line in [line.strip('\n') for line in open(filename)]:
        line_length = len(line)
        # if our position is greater than line length
        # we "repeat" the line, by setting the position back
        if position >= line_length:
            position -= line_length
        if line[position] == '#':
            num_trees += 1
        position += 3
    return num_trees


def test_task_two():
    assert task_two('test-data.txt') == 336
    assert task_two('real-data.txt') == 6818112000


def task_two(filename):
    # right, down values
    groups = [
        [1, 1],
        [3, 1],
        [5, 1],
        [7, 1],
        [1, 2]
    ]
    results = []
    lines = [line.strip('\n') for line in open(filename)]
    for group in groups:
        right, down = group
        position = num_trees = line_number = 0
        for line in lines:
            # skip lines based on down
            if line_number % down != 0:
                line_number += 1
                continue
            line_length = len(line)
            # if our position is greater than line length
            # we "repeat" the line, by setting the position back
            if position >= line_length:
                position -= line_length
            if line[position] == '#':
                num_trees += 1
            # update our position and line number for the next iteration
            position += right
            line_number += 1
        results.append(num_trees)
    total = 1
    for result in results:
        total = total * result
    return total
