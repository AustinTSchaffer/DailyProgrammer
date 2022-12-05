"""
    generateStacks()::Vector{Vector{Char}}

Generates the stacks for the problem input.

Each index "i" refers to "Stack i". The last index
of each stack is the "top" of that stack.

TODO: Ask the data engineering team to serialize their
representation of the stacks using JSON.
"""
function generateStacks()::Vector{Vector{Char}}
    return map(collect, [
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

Generates the stacks for the problem sample input.

Each index "i" refers to "Stack i". The last index
of each stack is the "top" of that stack.
"""
function generateSampleStacks()::Vector{Vector{Char}}
    return map(collect, [
        "ZN",
        "MCD",
        "P",
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
    fromstack = stacks[instruction.from]
    lastidx = length(fromstack)
    itemsToMove = splice!(fromstack, ((lastidx - instruction.qty) + 1):lastidx)
    foreach(char -> push!(stacks[instruction.to], char), Iterators.reverse(itemsToMove))
end

"""
    applyInstructionP2!(stacks::Vector{Vector{Char}}, instruction::Instruction)

Applies the instruction to the input "stacks", altering it in-place.
"qty" crates removed from the top of the "from" stack are placed onto the top
of the "to" stack.

This function moves the crates assuming all crates are moved simultaneously.
"""
function applyInstructionP2!(stacks::Vector{Vector{Char}}, instruction::Instruction)
    fromstack = stacks[instruction.from]
    lastidx = length(fromstack)
    itemsToMove = splice!(fromstack, ((lastidx - instruction.qty) + 1):lastidx)
    foreach(char -> push!(stacks[instruction.to], char), itemsToMove)
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

"""
Applies the given instructions to the 
"""
function moveContainers!(
    stacks::Vector{Vector{Char}},
    instructions::Vector{Instruction},
    applyInstruction!,
    )::String

    foreach(i -> applyInstruction!(stacks, i), instructions)
    return String(map(last, stacks))
end

function part1!(stacks::Vector{Vector{Char}}, instructions::Vector{Instruction})::String
    foreach(i -> applyInstructionP1!(stacks, i), instructions)
    return String(map(last, stacks))
end

function part2!(stacks::Vector{Vector{Char}}, instructions::Vector{Instruction})::String
    foreach(i -> applyInstructionP2!(stacks, i), instructions)
    return String(map(last, stacks))
end

sampleInstructions = loadInstructions("./sample_instructions.txt")

println("Part 1 (sample): ", part1!(generateSampleStacks(), sampleInstructions))
println("Part 2 (sample): ", part2!(generateSampleStacks(), sampleInstructions))

instructions = loadInstructions("./instructions.txt")

println("Part 1: ", part1!(generateStacks(), instructions))
println("Part 2: ", part2!(generateStacks(), instructions))
