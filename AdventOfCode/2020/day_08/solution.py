#%%

puzzle_input = open("./puzzle_input.txt").readlines()
puzzle_input = list(map(str.strip, puzzle_input))

#%%

instructions = []
for statement in puzzle_input:
    instruction, value = statement.split(" ")
    instructions.append((instruction, int(value)))

#%% Part 1

accumulator = 0
instructions_executed = set()
pc = 0

while pc not in instructions_executed:
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

print(accumulator)

# %%
