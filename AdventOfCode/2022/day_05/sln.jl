"""
    generateStacks()::Vector{Vector{Char}}

Generates the stacks for the problem input. Each index
"i" refers to "Stack i". Index 1 of each stack is the
"top" of that stack.
"""
function generateStacks()::Vector{Vector{Char}}
    return map(s -> collect(reverse(s)), [
        "SLW",
        "JTNQ",
        "SCHFJ",
        "TRMWNGB",
        "TRLSDHQB",
        "MJBVFHRL",
        "DWRNJM",
        "BZTFHNDJ",
        "HLQNBFT",
    ])
end

"""
    generateSampleStacks()::Vector{Vector{Char}}


"""
function generateSampleStacks()::Vector{Vector{Char}}
    return map(s -> collect(reverse(s)), [
        "SLW",
        "JTNQ",
        "SCHFJ",
        "TRMWNGB",
        "TRLSDHQB",
        "MJBVFHRL",
        "DWRNJM",
        "BZTFHNDJ",
        "HLQNBFT",
    ])
end

"""
Specifies a quantity of crates to move from the top of
one stack to the top of another stack. The order of how
those crates are applied to the top of the "to" stack
is not specified.
"""
struct Instruction
    qty::Int
    from::Int
    to::Int
end

"""
    applyInstructionP1!(stacks::Vector{Vector{Char}}, instruction::Instruction)

Applies the instruction to the input "stacks", altering it in-place.
"qty" crates removed from the top of the "from" stack are placed onto the top
of the "to" stack.

This function moves crates using the "towers of hanoi" methodology.
"""
function applyInstructionP1!(stacks::Vector{Vector{Char}}, instruction::Instruction)
    result = splice!(stacks[instruction.from], 1:instruction.qty)
    foreach(char -> insert!(stacks[instruction.to], 1, char), result)
end

"""
    applyInstructionP2!(stacks::Vector{Vector{Char}}, instruction::Instruction)

Applies the instruction to the input "stacks", altering it in-place.
"qty" crates removed from the top of the "from" stack are placed onto the top
of the "to" stack.

This function moves the crates assuming all crates are moved simultaneously.
"""
function applyInstructionP2!(stacks::Vector{Vector{Char}}, instruction::Instruction)
    result = splice!(stacks[instruction.from], 1:instruction.qty)
    foreach(char -> insert!(stacks[instruction.to], 1, char), Iterators.reverse(result))
end

"""
Parses instructions from a string, using the form `"move 1 from 6 to 4"`.
"""
function parseInstruction(move::String)::Instruction
    parts = split(move, ' ')
    return Instruction(
        parse(Int, parts[2]),
        parse(Int, parts[4]),
        parse(Int, parts[6]),
    )
end

"""
Loads all instructions from the specified file.
"""
function loadInstructions(filename::String)::Vector{Instruction}
    instructions::Vector{Instruction} = []

    open(filename, "r") do f
        for line in eachline(f)
            if all(isspace, line)
                continue
            end

            push!(instructions, parseInstruction(line))
        end
    end

    return instructions
end

function part1(instructions::Vector{Instruction})
    print("Part 1: ")
    part1_stacks = generateStacks()
    foreach(i -> applyInstructionP1!(part1_stacks, i), instructions)
    foreach(stack -> print(stack[1]), part1_stacks)
    println()
end

function part2(instructions::Vector{Instruction})
    print("Part 2: ")
    part2_stacks = generateStacks()
    foreach(i -> applyInstructionP2!(part2_stacks, i), instructions)
    foreach(stack -> print(stack[1]), part2_stacks)
    println()
end

instructions = loadInstructions("./instructions.txt")
part1(instructions)
part2(instructions)
