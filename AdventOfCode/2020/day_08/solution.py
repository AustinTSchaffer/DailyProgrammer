#%% Load and Decode Instructions

puzzle_input = open("./puzzle_input.txt").readlines()
puzzle_input = list(map(str.strip, puzzle_input))

instructions = []
for statement in puzzle_input:
    instruction, value = statement.split(" ")
    instructions.append((instruction, int(value)))

#%% Part 1

from typing import Tuple

def execute(instructions: list) -> Tuple[bool, int]:
    accumulator = 0
    instructions_executed = set()
    pc = 0

    while True:
        if pc == len(instructions):
            return True, accumulator

        if pc > len(instructions):
            return False, accumulator

        if pc in instructions_executed:
            return False, accumulator

        instruction, value = instructions[pc]
        instructions_executed.add(pc)

        if instruction == "nop":
            pc += 1
        elif instruction == "jmp":
            pc += value
        elif instruction == "acc":
            pc += 1
            accumulator += value
        else:
            raise ValueError(f"Invalid instruction '{instruction}'")

exited_properly, accumulator = execute(instructions)
assert exited_properly == False, "I thought this was still broken."

print("Part 1:", accumulator)

#%% Part 2

accumulator = 0

for instruction_index in range(len(instructions)):
    accumulator = 0
    instruction, value = instructions[instruction_index]

    if instruction == "nop":
        updated_instructions = instructions.copy()
        updated_instructions[instruction_index] = ("jmp", value)
        exited_properly, accumulator = execute(updated_instructions)
        if exited_properly:
            break

    if instruction == "jmp":
        updated_instructions = instructions.copy()
        updated_instructions[instruction_index] = ("nop", value)
        exited_properly, accumulator = execute(updated_instructions)
        if exited_properly:
            break

print("Part 2:", accumulator)
