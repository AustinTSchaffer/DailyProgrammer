# Solves Day 1 parts 1 and 2 using a single statement.

print(
    "\n".join(
        f"Part {n+1}: {result}"
        for n, result in
        enumerate(
           __import__("math").prod(next(
                combo
                for combo in
                __import__("itertools").combinations([
                    int(expense.strip())
                    for expense in
                    open("expenses.txt").readlines()
                ], number_of_values)
                if sum(combo) == 2020
            ))
            for number_of_values in
            range(2, 4)
        )
    )
)
