import re


REQ_FIELDS = {
    'byr': r'^(19[2-9][0-9]|200[0-2])$',
    'iyr': r'^(201[0-9]|2020)$',
    'eyr': r'^(202[0-9]|2030)$',
    'hgt': r'^((59in|6[0-9]in|7[0-6]in)|(1[5-8][0-9]cm|19[0-3]cm))$',
    'hcl': r'^#[a-f\d]{6}$',
    'ecl': r'^(amb|blu|brn|gry|grn|hzl|oth)$',
    'pid': r'^\d{9}$'
}


def test_task_one():
    assert task_one('test-data.txt') == 2
    assert task_one('real-data.txt') == 233


def task_one(filename):
    with open(filename, 'r') as file:
        lines = file.read().split('\n\n')
        num_valid = 0
        for line in lines:
            fields = [block.split(':')[0] for block in line.split()]
            if _check_for_required(fields):
                num_valid += 1
        return num_valid


def _check_for_required(fields):
    for req_field in REQ_FIELDS.keys():
        if req_field not in fields:
            return False
    return True


def test_task_two():
    assert task_two('invalid-passports.txt') == 0
    assert task_two('valid-passports.txt') == 4
    assert task_two('real-data.txt') == 111


def task_two(filename):
    with open(filename, 'r') as file:
        lines = file.read().split('\n\n')
        num_valid = 0
        for line in lines:
            blocks = line.split()
            fields = [block.split(':')[0] for block in blocks]
            if _check_for_required(fields) and _check_for_valid_fields(blocks):
                num_valid += 1
        return num_valid


def _check_for_valid_fields(fields):
    for field in fields:
        key, value = field.split(':')
        search = REQ_FIELDS.get(key)
        if search:
            match = re.search(search, value)
            if not match:
                return False
    return True
