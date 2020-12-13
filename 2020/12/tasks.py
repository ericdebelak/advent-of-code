DIRECTIONS = ['N', 'E', 'S', 'W']
TURNS = ['R', 'L']


def test_rotate():
    assert (1, -10) == _rotate('R', 90, 10, 1)
    assert (-1, 10) == _rotate('L', 90, 10, 1)
    assert (-10, -1) == _rotate('R', 180, 10, 1)
    assert (-10, -1) == _rotate('L', 180, 10, 1)
    assert (1, -10) == _rotate('L', 270, 10, 1)
    assert (-1, 10) == _rotate('R', 270, 10, 1)


def _rotate(turn, degrees, x, y):
    for turns in range(int(degrees / 90)):
        x, y = _rotate_ninety(turn, x, y)
    return x, y


def _rotate_ninety(turn, x, y):
    if turn == 'L':
        return -y, x
    else:
        return y, -x


def test_move_by_compass_direction():
    assert (0, 1) == _move_by_compass_direction('N', 1, 0, 0)
    assert (-1, 0) == _move_by_compass_direction('W', 1, 0, 0)


def _move_by_compass_direction(direction, value, x, y):
    # figure out if we should move positive or negative
    modifier = 1 if direction in ['N', 'E'] else -1
    if direction in ['N', 'S']:
        y += value * modifier
    else:
        x += value * modifier
    return x, y


def test_task_one():
    assert 25 == task_one('test-data.txt')
    assert 1294 == task_one('real-data.txt')


def task_one(filename):
    x = y = 0
    fx = 1  # facing east (negative would be west)
    fy = 0
    for action, value in map(lambda line: (line[0], int(line[1:])), open(filename)):
        if action in TURNS:
            fx, fy = _rotate(action, value, fx, fy)
        elif action in DIRECTIONS:
            x, y = _move_by_compass_direction(action, value, x, y)
        else:
            # move forward in the facing direction
            x += fx * value
            y += fy * value
    return abs(x) + abs(y)


def test_task_two():
    assert 286 == task_two('test-data.txt')
    assert 20592 == task_two('real-data.txt')


def task_two(filename):
    x = y = 0
    wx = 10
    wy = 1
    for action, value in map(lambda line: (line[0], int(line[1:])), open(filename)):
        if action in TURNS:
            wx, wy = _rotate(action, value, wx, wy)
        elif action in DIRECTIONS:
            wx, wy = _move_by_compass_direction(action, value, wx, wy)
        else:
            # move toward waypoint
            x += wx * value
            y += wy * value
    return abs(x) + abs(y)
