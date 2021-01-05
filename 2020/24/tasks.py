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


def test_get_number_of_black_adjacent():
    grid = {
        (0, 0): True,
        (.5, 1): True,
        (-1, 0): True
    }
    assert _get_number_of_black_adjacent(grid, (-.5, 1)) == 3
    assert _get_number_of_black_adjacent(grid, (-.5, -1)) == 2
    assert _get_number_of_black_adjacent(grid, (.5, -1)) == 1


def _get_number_of_black_adjacent(grid, coordinates):
    neighbors = _get_neighbors(coordinates)
    return sum([1 for neighbor in neighbors if neighbor in grid])


def _get_neighbors(coordinates):
    return [
        (coordinates[0] - .5, coordinates[1] + 1),
        (coordinates[0] + .5, coordinates[1] + 1),
        (coordinates[0] - .5, coordinates[1] - 1),
        (coordinates[0] + .5, coordinates[1] - 1),
        (coordinates[0] + 1, coordinates[1]),
        (coordinates[0] - 1, coordinates[1])
    ]


def test_is_black():
    grid = {
        (0, 0): True,
        (.5, 1): True,
        (-1, 0): True
    }
    assert _is_black(grid, (0, 0))
    assert _is_black(grid, (-.5, -1))


def _is_black(grid, coordinates):
    black_neighbors = _get_number_of_black_adjacent(grid, coordinates)
    if coordinates in grid and 0 < black_neighbors <= 2:
        return True
    elif coordinates not in grid and black_neighbors == 2:
        return True
    return False


def test_task_two():
    assert task_two('test-data.txt') == 2208
    assert task_two('real-data.txt') == 3636


def task_two(filename):
    grid = {}
    for line in open(filename):
        coordinates = _traverse_grid(line.rstrip())
        if coordinates in grid:
            del grid[coordinates]
        else:
            grid[coordinates] = True
    for i in range(100):
        new_grid = {}
        for tile in grid.keys():
            if _is_black(grid, tile):
                new_grid[tile] = True
            # go through only neighbors of black tiles
            white_neighbors = [neighbor for neighbor in _get_neighbors(tile) if neighbor not in grid]
            for neighbor in white_neighbors:
                if _is_black(grid, neighbor):
                    new_grid[neighbor] = True
        grid = new_grid
    return len(grid)
