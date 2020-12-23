from collections import deque


def test_task_one():
    assert task_one('389125467') == '67384529'
    assert task_one('789465123') == '98752463'


def task_one(cups):
    cups = deque(int(x) for x in cups)
    highest_cup = max(cups)
    for _ in range(100):
        current = cups[0]
        # shift list so current is at the end
        cups.rotate(-1)
        picked_up = deque()
        for _ in range(3):
            picked_up.append(cups.popleft())
        # get the destination
        for i in range(1, current + 1):
            if current - i == 0:
                destination = max(cups)
                break
            elif current - i in cups:
                destination = current - i
                break
        # re-add our picked up in reversed order so we add the last one first then second then first
        picked_up.reverse()
        for cup in picked_up:
            # insert our picked up cups after the destination
            cups.insert(cups.index(destination) + 1, cup)
    # rotate to 1 being first
    cups.rotate(-cups.index(1))
    # remove 1
    cups.popleft()
    return "".join([str(cup) for cup in cups])


def test_task_two():
    assert task_two('389125467') == 149245887792
    assert task_two('789465123') == 2000455861


def task_two(cups):
    initial_cups = [int(x) for x in cups]
    # key is cup, value is next cup
    cups = {}
    for index, cup in enumerate(initial_cups):
        if index < len(initial_cups) - 1:
            cups[cup] = initial_cups[index + 1]
        else:
            # this will be the first value in the numeric order numbers
            cups[cup] = 10
    # set 10 - 999999
    for i in range(len(initial_cups) + 1, 1000000):
        cups[i] = i + 1

    # set our last cup to have the first cup as next
    cups[1000000] = initial_cups[0]

    current = initial_cups[0]

    for _ in range(10000000):
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
                destination = max(cups)
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

    # our two cups with stars are the ones after 1
    first_cup_with_star = cups[1]
    second_cup_with_star = cups[first_cup_with_star]
    return first_cup_with_star * second_cup_with_star
