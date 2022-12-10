struct Instruction
    orig::String
    addx::Int
    cycles::Int
end

function parseInstructions(data::Vector{String})::Vector{Instruction}
    return map(
        line -> begin
            s = split(line, ' ')
            if s[1] == "noop"
                Instruction(line, 0, 1)
            else
                Instruction(line, parse(Int, s[2]), 2)
            end
        end,
        data
    )
end

instructions = parseInstructions(readlines(open("input.txt")))
sample_input_1 = parseInstructions(readlines(open("sample_input_1.txt")))
sample_input_2 = parseInstructions(readlines(open("sample_input_2.txt")))

function compute(instructions::Vector{Instruction}; init=1)::Vector{Int}
    x = init
    xvalues = Vector{Int}()
    for instruction in instructions
        for _ in range(1, instruction.cycles)
            push!(xvalues, x)
        end
        x += instruction.addx
    end
    push!(xvalues, x)

    return xvalues
end

computeResult = compute(instructions)

# The collect(enumerate(x)) is because Julia doesn't have a "filter enumeration"
# https://github.com/JuliaLang/julia/issues/45337
part_1 = sum(prod, filter(
    pair -> (pair[1] + 20) % 40 == 0,
    collect(enumerate(computeResult))
))

println("Part 1: ", part_1)

screen = Vector{Char}()
for (idx, spritepos) in enumerate(computeResult)
    hpos = ((idx - 1) % 40) + 1
    activePixel = hpos in spritepos:(spritepos+2)
    push!(screen, activePixel ? '#' : '.')
end

println("Part 2: ")

using IterTools
for line in partition(screen, 40)
    println(join(line))
end
