def test_get_loop_size():
    assert _get_loop_size(5764801) == 8
    assert _get_loop_size(17807724) == 11


def _get_loop_size(subject_number):
    number = 1
    i = 0
    while number != subject_number:
        number = (number * 7) % 20201227
        i += 1
    return i


def test_get_encryption_key():
    assert _get_encryption_key(8, 17807724) == 14897079
    assert _get_encryption_key(11, 5764801) == 14897079


def _get_encryption_key(loop_size, public_key):
    encryption_key = 1
    for i in range(loop_size):
        encryption_key = (encryption_key * public_key) % 20201227
    return encryption_key


def test_task_one():
    assert task_one('test-data.txt') == 14897079
    assert task_one('real-data.txt') == 4441893


def task_one(filename):
    [card_key, door_key] = [int(line.rstrip()) for line in open(filename)]
    card_loop_size = _get_loop_size(card_key)
    card_encryption_key = _get_encryption_key(card_loop_size, door_key)
    return card_encryption_key
