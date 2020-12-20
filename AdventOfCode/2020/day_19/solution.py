#%% Part 1

from data import rules, messages
from data import test_rules, test_messages

def build_regex(rules: dict, rule_id: str):
    def _build_regex(rule_id: str):
        rule = rules[rule_id]
        if isinstance(rule, str):
            return rule
        else:
            regexes = [
                "".join(
                    _build_regex(term)
                    for term in subrule
                )
                for subrule in rule
            ]

            return "(" + "|".join(
                f"({regex})"
                for regex in regexes
            ) + ")"

    return r"^(" + _build_regex(rule_id) + r")$"

import re
RULE_ZERO_REGEX = re.compile(build_regex(rules, '0'))
TEST_RULE_ZERO_REGEX = re.compile(build_regex(test_rules, '0'))

print("Part 1 Test:", len(list(filter(TEST_RULE_ZERO_REGEX.match, test_messages))))
print("Part 1:", len(list(filter(RULE_ZERO_REGEX.match, messages))))

#%% Part 2

from data import parse_rule

part_2_rules = rules.copy()
parse_rule(part_2_rules, "8: 42 | 42 8")
parse_rule(part_2_rules, "11: 42 31 | 42 11 31")

def build_regex_part_2(rules: dict, rule_id: str, max_rule_11_depth: int=12):
    def _build_regex(rule_id: str, rule_11_depth: int):
        if rule_id == "8":
            return "{}+".format(_build_regex("42", rule_11_depth))

        if rule_id == "11":
            return f"{_build_regex('42', rule_11_depth)}{{{rule_11_depth}}}{_build_regex('31', rule_11_depth)}{{{rule_11_depth}}}"

        rule = rules[rule_id]
        if isinstance(rule, str):
            return rule
        else:
            regexes = [
                "".join(
                    _build_regex(term, rule_11_depth)
                    for term in subrule
                )
                for subrule in rule
            ]

            return "(" + "|".join(
                f"({regex})"
                for regex in regexes
            ) + ")"

    return [
        r"^(" + _build_regex(rule_id, rule_11_depth) + r")$"
        for rule_11_depth in range(1, max_rule_11_depth + 2)
    ]

RULE_ZERO_REGEXES = [
    re.compile(regex)
    for regex in
    build_regex_part_2(part_2_rules, '0')
]

part_2_messages = [
    message
    for message in messages
    if any(
        regex.match(message)
        for regex in RULE_ZERO_REGEXES
    )
]

print("Part 2:", len(part_2_messages))
