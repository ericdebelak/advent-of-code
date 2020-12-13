import math


def test_get_seat_number():
    assert 357 == _get_seat_number('FBFBBFFRLR')
    assert 567 == _get_seat_number('BFFFBBFRRR')
    assert 119 == _get_seat_number('FFFBBBFRRR')
    assert 820 == _get_seat_number('BBFFBBFRLL')


def _get_seat_number(boarding_pass):
    row_upper = 127
    seat_upper = 7
    row_lower = seat_lower = final_row = 0
    for index in range(len(boarding_pass)):
        char = boarding_pass[index]
        if index == 6:
            final_row = row_lower if char == 'F' else row_upper
        elif index == 9:
            final_seat = seat_lower if char == 'L' else seat_upper
            return final_row * 8 + final_seat
        elif char == 'F':
            row_upper = math.floor(_get_middle(row_lower, row_upper))
        elif char == 'B':
            row_lower = round(_get_middle(row_lower, row_upper))
        elif char == 'L':
            seat_upper = math.floor(_get_middle(seat_lower, seat_upper))
        elif char == 'R':
            seat_lower = round(_get_middle(seat_lower, seat_upper))


def _get_middle(lower, upper):
    return lower + (upper - lower) / 2


def test_task_one():
    assert 820 == task_one('test-data.txt')
    assert 959 == task_one('real-data.txt')


def task_one(filename):
    return max([_get_seat_number(line) for line in open(filename)])


def test_task_two():
    assert 527 == task_two('real-data.txt')


def task_two(filename):
    seats = [_get_seat_number(line) for line in open(filename)]
    for i in range(min(seats), max(seats)):
        if i not in seats and i - 1 in seats and i + 1 in seats:
            return i
    return False
