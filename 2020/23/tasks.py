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
