def test_get_question_count():
    assert 3 == _get_question_count('a\nb\nc')
    assert 3 == _get_question_count('abc')
    assert 3 == _get_question_count('ab\nac')


def _get_question_count(text):
    answered_questions = []
    for line in text.splitlines():
        for char in line:
            if char not in answered_questions:
                answered_questions.append(char)
    return len(answered_questions)


def test_task_one():
    assert 11 == task_one('test-data.txt')
    assert 6683 == task_one('real-data.txt')


def task_one(filename):
    with open(filename, 'r') as file:
        lines = file.read().split('\n\n')
        total = 0
        for line in lines:
            total += _get_question_count(line)
        return total


def test_get_same_question_count():
    assert 0 == _get_same_question_count('a\nb\nc')
    assert 3 == _get_same_question_count('abc')
    assert 1 == _get_same_question_count('ab\nac')
    assert 1 == _get_question_count('a\na\na\na')
    assert 1 == _get_same_question_count('b')
    assert 0 == _get_same_question_count('icb\nxqhf')


def _get_same_question_count(text):
    lines = text.splitlines()
    # we should add all the questions for the first line
    answered_questions = [char for char in lines[0]]
    for line in lines:
        # build list with all questions that also occur in the current line
        answered_questions = [question for question in answered_questions if question in line]
    return len(answered_questions)


def test_task_two():
    assert 6 == task_two('test-data.txt')
    assert 3122 == task_two('real-data.txt')


def task_two(filename):
    with open(filename, 'r') as file:
        lines = file.read().split('\n\n')
        total = 0
        for line in lines:
            total += _get_same_question_count(line)
        return total
