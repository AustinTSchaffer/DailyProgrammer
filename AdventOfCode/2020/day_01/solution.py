# Solves Day 1 parts 1 and 2, using only 2
# expressions without repeating any code.

print(
    "Part 1:",
    __import__("math").prod([
        combo for combo in
        __import__("itertools").combinations([
            int(expense.strip())
            for expense in
            open("expenses.txt").readlines()
        ], int(2.0))
        if sum(combo) == 2020
    ][0])
)

exec(
    open("solution.py")
        .read()
        .replace("Part 1", "Part 2")
        .replace("2.0", "3.0")
        .replace("exec", "")
)
