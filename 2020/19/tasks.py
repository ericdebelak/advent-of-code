import re


def test_task_one():
    assert task_one('test-data.txt') == 2
    assert task_one('real-data.txt') == 230


def task_one(filename):
    with open(filename, 'r') as file:
        rule_lines, message_lines = file.read().split('\n\n')
        rules_graph = {}
        messages = message_lines.splitlines()
        for line in rule_lines.splitlines():
            key, rule = line.split(':')
            rules_graph[key] = rule.strip()

        rules_parsed = {}
        while '0' not in rules_parsed:  # once we get all the numbers we need for 0, we can proceed
            for rule_index, rule in rules_graph.items():
                if rule_index in rules_parsed:
                    continue
                if '"' in rule:
                    rules_parsed[rule_index] = rule.strip('"')  # this is just a letter, add it to the rules
                else:
                    numbers = re.findall(r'(\d+)', rule)  # get all rule numbers in this rule
                    numbers.sort(reverse=True)  # sort to get the larger digits first to not replace the wrong one
                    # if we have all the previous number parsed, substitute the parsed rule for each number
                    if all([number in rules_parsed for number in numbers]):
                        for number in numbers:
                            rules_graph[rule_index] = rules_graph[rule_index].replace(number, rules_parsed[number])
                        # now that the rules are pared, we can ditch the spaces
                        rules_graph[rule_index] = rules_graph[rule_index].replace(' ', '')
                        # add parens to group if there is a pipe
                        if '|' in rule:
                            rules_graph[rule_index] = '(' + rules_graph[rule_index] + ')'
                        # update our parsed rules
                        rules_parsed[rule_index] = rules_graph[rule_index]
        return sum([bool(re.fullmatch(rules_parsed['0'], message)) for message in messages])


def test_task_two():
    assert task_two('real-data.txt') == 341


def task_two(filename):
    with open(filename, 'r') as file:
        rule_lines, message_lines = file.read().split('\n\n')
        rules_graph = {}
        messages = message_lines.splitlines()
        for line in rule_lines.splitlines():
            key, rule = line.split(':')
            rules_graph[key] = rule.strip()

        rules_parsed = {}
        while '0' not in rules_parsed:  # once we get all the numbers we need for 0, we can proceed
            for rule_index, rule in rules_graph.items():
                if '"' in rule:
                    rules_parsed[rule_index] = rule.strip('"')  # this is just a letter, add it to the rules
                else:
                    # add our new rules
                    if rule_index == '8' and '42' in rules_parsed:
                        rules_parsed[rule_index] = rules_parsed['42'] + '+'
                    elif rule_index == '11' and '42' in rules_parsed and '31' in rules_parsed:
                        rule_text = '('
                        # build a list of (42{1}31{1}|42{2}31{2}...)
                        for i in range(1, 11):
                            rule_text += rules_parsed['42'] + \
                                         '{' + str(i) + '}' + \
                                         rules_parsed['31'] + \
                                         '{' + str(i) + '}|'
                        # strip the final | and add a )
                        rules_parsed[rule_index] = rule_text[0:-1] + ')'
                    else:
                        numbers = re.findall(r'(\d+)', rule)  # get all rule numbers in this rule
                        numbers.sort(reverse=True)  # sort to get the larger digits first to not replace the wrong one
                        # if we have all the previous number parsed, substitute the parsed rule for each number
                        if all([number in rules_parsed for number in numbers]):
                            for number in numbers:
                                rules_graph[rule_index] = rules_graph[rule_index].replace(number, rules_parsed[number])
                            # now that the rules are pared, we can ditch the spaces
                            rules_graph[rule_index] = rules_graph[rule_index].replace(' ', '')
                            # add parens to group if there is a pipe
                            if '|' in rule:
                                rules_graph[rule_index] = '(' + rules_graph[rule_index] + ')'
                            # update our parsed rules
                            rules_parsed[rule_index] = rules_graph[rule_index]
        return sum([bool(re.fullmatch(rules_parsed['0'], message)) for message in messages])
