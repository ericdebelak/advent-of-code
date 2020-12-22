def _parse_decks(file):
    decks = []
    groups = file.read().split('\n\n')
    for group in groups:
        lines = group.splitlines()
        decks.append([int(x) for x in lines[1:]])
    return decks


def test_task_one():
    assert task_one('test-data.txt') == 306
    assert task_one('real-data.txt') == 31957


def task_one(filename):
    with open(filename, 'r') as file:
        decks = _parse_decks(file)
        while len(decks[0]) != 0 and len(decks[1]) != 0:
            length = min(len(decks[0]), len(decks[1]))
            for i in range(length):
                if decks[0][i] > decks[1][i]:
                    decks[0].append(decks[0][i])
                    decks[0].append(decks[1][i])
                else:
                    decks[1].append(decks[1][i])
                    decks[1].append(decks[0][i])

            decks[0] = decks[0][length:] if len(decks[0]) > 1 else []
            decks[1] = decks[1][length:] if len(decks[1]) > 1 else []
        score = 0
        winner = decks[0] if len(decks[0]) > len(decks[1]) else decks[1]
        for index, card in enumerate(winner):
            modifier = len(winner) - index
            score += card * modifier
    return score
