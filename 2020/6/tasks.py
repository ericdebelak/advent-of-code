def test_get_question_count():
    assert _get_question_count('a\nb\nc') == 3
    assert _get_question_count('abc') == 3
    assert _get_question_count('ab\nac') == 3


def _get_question_count(text):
    answered_questions = []
    for line in text.splitlines():
        for char in line:
            if char not in answered_questions:
                answered_questions.append(char)
    return len(answered_questions)


def test_task_one():
    assert task_one('test-data.txt') == 11
    assert task_one('real-data.txt') == 6683


def task_one(filename):
    with open(filename, 'r') as file:
        lines = file.read().split('\n\n')
        total = 0
        for line in lines:
            total += _get_question_count(line)
        return total


def test_get_same_question_count():
    assert _get_same_question_count('a\nb\nc') == 0
    assert _get_same_question_count('abc') == 3
    assert _get_same_question_count('ab\nac') == 1
    assert _get_question_count('a\na\na\na') == 1
    assert _get_same_question_count('b') == 1
    assert _get_same_question_count('icb\nxqhf') == 0


def _get_same_question_count(text):
    lines = text.splitlines()
    # we should add all the questions for the first line
    answered_questions = [char for char in lines[0]]
    for line in lines:
        # build list with all questions that also occur in the current line
        answered_questions = [question for question in answered_questions if question in line]
    return len(answered_questions)


def test_task_two():
    assert task_two('test-data.txt') == 6
    assert task_two('real-data.txt') == 3122


def task_two(filename):
    with open(filename, 'r') as file:
        lines = file.read().split('\n\n')
        total = 0
        for line in lines:
            total += _get_same_question_count(line)
        return total
