def parse_rule(rules: dict, rule: str):
    key, rule = rule.split(": ")
    key, rule = key.strip(), rule.strip()
    if rule in ('"a"', '"b"'):
        rules[key] = rule.strip('"')
    else:
        rules[key] = tuple(
            tuple(option.strip().split(" "))
            for option in rule.split("|")
        )

rules = {}
for line in open("data/rules.txt").readlines():
    parse_rule(rules, line)

messages = [
    str.strip(line) for line in
    open("data/messages.txt").readlines()
]

test_rules = {}
for line in open("data/test_rules.txt").readlines():
    parse_rule(test_rules, line)

test_messages = [
    str.strip(line) for line in
    open("data/test_messages.txt").readlines()
]
