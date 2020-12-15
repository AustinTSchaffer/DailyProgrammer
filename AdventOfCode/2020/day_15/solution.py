import collections

puzzle_input = (0,13,1,8,6,15)

test_inputs = [
    ([(0,3,6), 10], 0),
    ([(1,3,2)], 1),
    ([(2,1,3)], 10),
    ([(1,2,3)], 27),
    ([(2,3,1)], 78),
    ([(3,2,1)], 438),
    ([(3,1,2)], 1836),

    # Expensive Tests
    # ([(0,3,6), 30000000], 175594),
    # ([(1,3,2), 30000000], 2578),
    # ([(2,1,3), 30000000], 3544142),
    # ([(1,2,3), 30000000], 261214),
    # ([(2,3,1), 30000000], 6895259),
    # ([(3,2,1), 30000000], 18),
    # ([(3,1,2), 30000000], 362),
]

def iterate(input_, iterations=2020) -> int:
    turn = 0
    turn_last_spoken = collections.defaultdict(int)
    prev_number = None

    for value in input_:
        turn_last_spoken[prev_number] = turn
        prev_number = value
        turn += 1

    while turn < iterations:
        current_number = turn_last_spoken[prev_number]
        turn_last_spoken[prev_number] = turn
        if current_number != 0:
            current_number = turn - current_number

        prev_number = current_number
        turn += 1

    return prev_number

for _input, expected_output in test_inputs:
    print("Testing:", *_input, "...")
    actual_output = iterate(*_input)
    assert actual_output == expected_output, f"Expected: {expected_output}. Actual {actual_output}"

print("Part 1:", iterate(puzzle_input))
print("Part 2:", iterate(puzzle_input, 30000000))
