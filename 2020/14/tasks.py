from copy import copy


def test_task_one():
    assert task_one('test-data.txt') == 165
    assert task_one('real-data.txt') == 12512013221615


def task_one(filename):
    with open(filename, 'r') as file:
        mem = {}
        masks = _get_mask_array(file.read())
        for mask, values in masks:
            for key, value in values.items():
                binary_string = '{0:036b}'.format(value)
                for index, char in enumerate(mask):
                    if char == 'X':
                        continue
                    else:
                        binary_string = _adjust_binary_string(binary_string, index, char)
                mem[key] = int(binary_string, 2)
    return sum(mem.values())


def _adjust_binary_string(string, index, char):
    return string[:index] + char + string[index + 1:]


def _get_mask_array(text):
    masks = []
    groups = text.split('mask = ')
    for group in groups:
        if group:
            lines = group.splitlines()
            value_dict = {}
            values = lines[1:]
            for value in values:
                items = value.split(' = ')
                key = items[0].strip('mem[').strip(']')
                value_dict[int(key)] = int(items[1])
            masks.append((lines[0], value_dict))
    return masks


def _get_modifier(index):
    if index == 0:
        return 1
    return 2 * _get_modifier(index - 1)


def test_get_indexes_for_x():
    assert _get_indexes_for_x('000000000000000000000000000000X1001X') == [0, 5]


def _get_indexes_for_x(mask):
    reversed_mask = mask[::-1]
    return [i for i, char in enumerate(reversed_mask) if char == 'X']


def test_add_mem_permutations():
    assert _add_mem_permutations('000000000000000000000000000000X1001X', '000000000000000000000000000000011010', 100, {}) == {
        26: 100,
        27: 100,
        58: 100,
        59: 100
    }


def _add_mem_permutations(mask, binary_string_with_0, mem_value, mem):
    value_with_0s = int(binary_string_with_0, 2)  # this is our starting point, the permutation with all 0s
    previous_values = [value_with_0s]
    mem[value_with_0s] = mem_value
    x_indexes = _get_indexes_for_x(mask)  # get our indexes for x in reverse order, so we know where we change things
    for index in x_indexes:
        modifier = _get_modifier(index)  # our modifier is the value at that position in the binary string for 1
        previous = copy(previous_values)
        for value in previous:
            key = value + int(modifier)  # add our modifier for each previous value
            mem[key] = mem_value  # set the mem dict with the key and original value
            previous_values.append(key)
    return mem


def test_task_two():
    assert task_two('test-data-two.txt') == 208
    assert task_two('real-data.txt') == 3905642473893


def task_two(filename):
    with open(filename, 'r') as file:
        mem = {}
        masks = _get_mask_array(file.read())
        for mask, values in masks:
            for key, value in values.items():
                binary_string = '{0:036b}'.format(key)
                for index, char in enumerate(mask):
                    # apply our changes
                    if char == '1':
                        binary_string = _adjust_binary_string(binary_string, index, char)
                    elif char == 'X':
                        # for now, set 0 as our base
                        binary_string = _adjust_binary_string(binary_string, index, '0')
                mem = _add_mem_permutations(mask, binary_string, value, mem)
    return sum(mem.values())
