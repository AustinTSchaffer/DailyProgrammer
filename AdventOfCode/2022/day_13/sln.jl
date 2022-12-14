textInput = split(read(open("input.txt"), String), "\n", keepempty=false)

function parseInput(input::AbstractString)::Vector
    function closure!(current::Vector, index::Int)::Tuple{Vector, Int}
        currentNum::Union{Int, Nothing} = nothing
        i = index
        while i <= length(input)
            char = input[i]
            i += 1

            if char == ']'
                if currentNum !== nothing
                    push!(current, currentNum)
                end

                return current, i
            elseif char == '['
                vec, i = closure!([], i)
                push!(current, vec)
            elseif char in "0123456789"
                digitVal = Int(char - '0')
                currentNum = currentNum === nothing ? digitVal : (10 * currentNum) + digitVal
            elseif char == ','
                if currentNum !== nothing
                    push!(current, currentNum)
                    currentNum = nothing
                end
            else
                error("Idk what this is: ($char) ($(i - 1))")
            end
        end
    end

    result, _ = closure!([], 2)
    return result
end

function compare(a::Vector, b::Vector)::Int
    alen = length(a)
    blen = length(b)
    for i in 1:max(alen, blen)
        if i > alen
            return -1
        elseif i > blen
            return 1
        end

        aelem = a[i]
        belem = b[i]

        if isa(aelem, Int) && isa(belem, Int)
            if aelem < belem
                return -1
            elseif aelem > belem
                return 1
            end
        else
            result = compare(isa(aelem, Int) ? [aelem] : aelem, isa(belem, Int) ? [belem] : belem)
            if result != 0
                return result
            end
        end
    end

    return 0
end

input = map(parseInput, textInput)

pairwiseInput::Vector{Tuple{Vector, Vector}} = [
    (input[i], input[i+1])
    for i in 1:2:length(input)
]

incorrectOrderInputs = []
correctOrderInputs = []
for (idx, pair) in enumerate(pairwiseInput)
    if compare(pair[1], pair[2]) < 0
        push!(correctOrderInputs, (idx, pair))
    else
        push!(incorrectOrderInputs, (idx, pair))
    end
end

println("Part 1: ", sum(ipair -> ipair[1], correctOrderInputs))

divPacket1::Vector{Any} = [[2]]
divPacket2::Vector{Any} = [[6]]

allPackets = sort([divPacket1, divPacket2, input...], lt=(a, b) -> compare(a, b) == -1)

println("Part 2: ", findfirst(x -> x == divPacket1, allPackets), findfirst(x -> x == divPacket2, allPackets))
