def test_traverse_grid():
    assert _traverse_grid('nwwswee') == (0, 0)
    assert _traverse_grid('esew') == (.5, -1)


def _traverse_grid(directions, coordinates=(0,0)):
    if len(directions) == 0:
        return coordinates
    if directions.startswith('nw'):
        new_coordinates = (coordinates[0] - .5, coordinates[1] + 1)
        return _traverse_grid(directions[2:], new_coordinates)
    if directions.startswith('ne'):
        new_coordinates = (coordinates[0] + .5, coordinates[1] + 1)
        return _traverse_grid(directions[2:], new_coordinates)
    if directions.startswith('sw'):
        new_coordinates = (coordinates[0] - .5, coordinates[1] - 1)
        return _traverse_grid(directions[2:], new_coordinates)
    if directions.startswith('se'):
        new_coordinates = (coordinates[0] + .5, coordinates[1] - 1)
        return _traverse_grid(directions[2:], new_coordinates)
    if directions.startswith('e'):
        new_coordinates = (coordinates[0] + 1, coordinates[1])
        return _traverse_grid(directions[1:], new_coordinates)
    if directions.startswith('w'):
        new_coordinates = (coordinates[0] - 1, coordinates[1])
        return _traverse_grid(directions[1:], new_coordinates)


def test_task_one():
    assert task_one('test-data.txt') == 10
    assert task_one('real-data.txt') == 287


def task_one(filename):
    grid = {}
    for line in open(filename):
        coordinates = _traverse_grid(line.rstrip())
        if coordinates in grid:
            del grid[coordinates]
        else:
            grid[coordinates] = True
    return len(grid)
