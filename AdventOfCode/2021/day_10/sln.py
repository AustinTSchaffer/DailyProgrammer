import common
lines = common.get_input(__file__, str.strip)

open_ = "{[(<"
close_ = "}])>"
paren_mapper = {
    "}": "{",
    "{": "}",
    "]": "[",
    "[": "]",
    ")": "(",
    "(": ")",
    ">": "<",
    "<": ">",
}

illegal_character_scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

incomplete_character_scrores = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}

incomplete_lines = []
invalid_lines = []
for line in lines:
    corruption_found = False
    stack = [] # Last element is top of stack
    for char in line:
        if char in open_:
            stack.append(char)
        if char in close_:
            if stack.pop(-1) != paren_mapper[char]:
                invalid_lines.append({
                    "line": line,
                    "expected": paren_mapper[stack[-1]],
                    "actual": char,
                })
                corruption_found = True
                break

    if not corruption_found:
        closing_score = 0
        for char in reversed(stack):
            closing_score = (5 * closing_score) + incomplete_character_scrores[paren_mapper[char]]

        incomplete_lines.append({
            "line": line,
            "closing_score": closing_score,
        })

illegal_character_score = 0
for line in invalid_lines:
    illegal_character_score += illegal_character_scores[line["actual"]] 

print("Part 1:", illegal_character_score)

incomplete_lines_sorted = sorted(incomplete_lines, key=lambda icline: icline["closing_score"])

print("Part 2:", incomplete_lines_sorted[(len(incomplete_lines) // 2)])
