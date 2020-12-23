def _make_moves(initial_cups, rounds):
    # key is cup, value is next cup
    cups = {}
    for index, cup in enumerate(initial_cups):
        if index < len(initial_cups) - 1:
            # add the next cup
            cups[cup] = initial_cups[index + 1]
        else:
            # end of list, add the first cup
            cups[cup] = initial_cups[0]

    current = initial_cups[0]

    for _ in range(rounds):
        # pick up our next three cups from current
        first = cups[current]
        second = cups[first]
        third = cups[second]

        # reset the next cup on current to be the one after the third picked up cup
        cups[current] = cups[third]

        picked_up = [first, second, third]
        # get the destination
        for i in range(1, current + 1):
            if current - i == 0:
                destination = max([cup for cup in cups if cup not in picked_up])
                break
            elif current - i not in picked_up:
                destination = current - i
                break
        # the cup after our destination now is after our third picked up cup
        cups[third] = cups[destination]
        # the first and second cups have the same cups after them
        # the destination's next cup is now the first cup picked up
        cups[destination] = first
        current = cups[current]
    return cups


def test_task_one():
    assert task_one('389125467') == '67384529'
    assert task_one('789465123') == '98752463'


def task_one(cups):
    initial_cups = [int(x) for x in cups]

    cups = _make_moves(initial_cups, 100)
    cup_string = ''
    next_cup = cups[1]
    while next_cup != 1:
        cup_string += str(next_cup)
        next_cup = cups[next_cup]
    return cup_string


def test_task_two():
    assert task_two('389125467') == 149245887792
    assert task_two('789465123') == 2000455861


def task_two(cups):
    initial_cups = [int(x) for x in cups]

    for i in range(len(initial_cups) + 1, 1000001):
        initial_cups.append(i)

    cups = _make_moves(initial_cups, 10000000)

    # our two cups with stars are the ones after 1
    first_cup_with_star = cups[1]
    second_cup_with_star = cups[first_cup_with_star]
    return first_cup_with_star * second_cup_with_star
