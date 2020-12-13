import itertools
from copy import copy


FLOOR = '.'
EMPTY = 'L'
OCCUPIED = '#'


def test_get_count_adjacent():
    rows = [
        [FLOOR, OCCUPIED, EMPTY],
        [OCCUPIED, EMPTY, EMPTY],
        [FLOOR, OCCUPIED, EMPTY],
    ]
    assert 3 == _count_adjacent(rows, 1, 1)
    assert 2 == _count_adjacent(rows, 1, 2)
    assert 1 == _count_adjacent(rows, 2, 2)


def _count_adjacent(rows, row_index, column_index):
    count = 0
    rows_to_check = _build_list_to_check(row_index, len(rows))
    columns_to_check = _build_list_to_check(column_index, len(rows[0]))
    for row_to_check in rows_to_check:
        for column_to_check in columns_to_check:
            # we don't count our current one
            if row_to_check == row_index and column_to_check == column_index:
                continue
            elif rows[row_to_check][column_to_check] == OCCUPIED:
                count += 1
    return count


def _build_list_to_check(index, length):
    return [index + x for x in [-1, 0, 1] if length > index + x >= 0]


def _apply_rules(rows, max_adjacent, adjacent_method):
    new_rows = copy(rows)
    has_changed = False
    column_range = range(len(rows[0]))
    for row_index in range(len(rows)):
        for column_index in column_range:
            seat_type = rows[row_index][column_index]
            if seat_type == FLOOR:
                continue
            adjacent_count = adjacent_method(rows, row_index, column_index)
            if seat_type == OCCUPIED and adjacent_count >= max_adjacent:
                new_rows[row_index] = _update_row(new_rows[row_index], column_index, EMPTY)
                has_changed = True
            elif seat_type == EMPTY and adjacent_count == 0:
                new_rows[row_index] = _update_row(new_rows[row_index], column_index, OCCUPIED)
                has_changed = True
    return has_changed, new_rows


def _update_row(row, column_index, new_string):
    return row[:column_index] + new_string + row[column_index+1:]


def test_task_one():
    assert 37 == task_one('test-data.txt')
    assert 2178 == task_one('real-data.txt')


def task_one(filename):
    rows = [line.strip('\n') for line in open(filename)]
    has_changed = True
    while has_changed:
        has_changed, rows = _apply_rules(rows, 4, _count_adjacent)
    return sum([row.count('#') for row in rows])


def test_count_adjacent_two():
    rows = [
        '.......#.',
        '...#.....',
        '.#.......',
        '.........',
        '..#L....#',
        '....#....',
        '.........',
        '#........',
        '...#.....'
    ]
    assert 8 == _count_adjacent_two(rows, 4, 3)
    rows = [
        '.............',
        '.L.L.#.#.#.#.',
        '.............'
    ]
    assert 0 == _count_adjacent_two(rows, 1, 1)
    rows = [
        '.##.##.',
        '#.#.#.#',
        '##...##',
        '...L...',
        '##...##',
        '#.#.#.#',
        '.##.##.'
    ]
    assert 0 == _count_adjacent_two(rows, 3, 3)


def _count_adjacent_two(rows, row_index, column_index):
    count = 0
    row_length = len(rows)
    column_length = len(rows[0])
    possible_directions = list(itertools.product([-1, 0, 1], repeat=2))
    # we don't want a direction that won't move
    possible_directions.remove((0, 0))
    for row_direction, column_direction in possible_directions:
        row_to_check = row_index + row_direction
        column_to_check = column_index + column_direction
        seat_found = False
        while (0 <= row_to_check < row_length and 0 <= column_to_check < column_length) and not seat_found:
            seat_type = rows[row_to_check][column_to_check]
            if seat_type == OCCUPIED:
                count += 1
                seat_found = True
            elif seat_type == EMPTY:
                seat_found = True
            column_to_check += column_direction
            row_to_check += row_direction
    return count


def test_task_two():
    assert 26 == task_two('test-data.txt')
    assert 1978 == task_two('real-data.txt')


def task_two(filename):
    rows = [line.strip('\n') for line in open(filename)]
    has_changed = True
    while has_changed:
        has_changed, rows = _apply_rules(rows, 5, _count_adjacent_two)
    return sum([row.count('#') for row in rows])
