from copy import copy


def _parse_decks(file):
    decks = []
    groups = file.read().split('\n\n')
    for group in groups:
        lines = group.splitlines()
        decks.append([int(x) for x in lines[1:]])
    return decks


def _play_game(decks):
    while len(decks[0]) != 0 and len(decks[1]) != 0:
        if decks[0][0] > decks[1][0]:
            decks[0].append(decks[0][0])
            decks[0].append(decks[1][0])
        else:
            decks[1].append(decks[1][0])
            decks[1].append(decks[0][0])
        decks[0] = decks[0][1:]
        decks[1] = decks[1][1:]
    return decks


def test_task_one():
    assert task_one('test-data.txt') == 306
    assert task_one('real-data.txt') == 31957


def task_one(filename):
    with open(filename, 'r') as file:
        decks = _parse_decks(file)
        decks = _play_game(decks)
        score = 0
        winner = decks[0] if len(decks[0]) > len(decks[1]) else decks[1]
        for index, card in enumerate(winner):
            modifier = len(winner) - index
            score += card * modifier
    return score


def _play_game_recursive(decks):
    previous_rounds = []
    while len(decks[0]) != 0 and len(decks[1]) != 0:
        if [decks[0], decks[1]] in previous_rounds:
            # player one wins the game
            return [[1], []]
        previous_rounds.append([copy(decks[0]), copy(decks[1])])
        if decks[0][0] < len(decks[0]) and decks[1][0] < len(decks[1]):
            new_decks = _play_game_recursive([decks[0][1:(decks[0][0] + 1)], decks[1][1:(decks[1][0] + 1)]])
            if len(new_decks[0]) > len(new_decks[1]):
                # player one wins
                decks[0].append(decks[0][0])
                decks[0].append(decks[1][0])
            else:
                # player two wins
                decks[1].append(decks[1][0])
                decks[1].append(decks[0][0])
        elif decks[0][0] > decks[1][0]:
            decks[0].append(decks[0][0])
            decks[0].append(decks[1][0])
        else:
            decks[1].append(decks[1][0])
            decks[1].append(decks[0][0])
        decks[0] = decks[0][1:]
        decks[1] = decks[1][1:]
    return decks


def test_task_two():
    assert task_two('test-data.txt') == 291
    assert task_two('real-data.txt') == 33212


def task_two(filename):
    with open(filename, 'r') as file:
        decks = _parse_decks(file)
        decks = _play_game_recursive(decks)
        score = 0
        winner = decks[0] if len(decks[0]) > len(decks[1]) else decks[1]
        for index, card in enumerate(winner):
            modifier = len(winner) - index
            score += card * modifier
    return score
