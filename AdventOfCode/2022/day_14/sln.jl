using IterTools

function loadBarriers(filename::String)::Vector{Vector{CartesianIndex}}
    input = split(read(open(filename), String), '\n', keepempty=false)

    barriers = Vector{Vector{CartesianIndex}}()
    for line in input
        barrier = Vector{CartesianIndex}()
        push!(barriers, barrier)
        x = split(line, " -> ")
        for _x in x
            push!(barrier, CartesianIndex(map(i -> parse(Int, i), split(_x, ','))...))
        end
    end

    return barriers
end

function processBarriers(barriers::Vector{Vector{CartesianIndex}})::Set{CartesianIndex}
    barrierIndexes = Set{CartesianIndex}()

    for barrier in barriers
        for pair in partition(barrier, 2, 1)
            diff = pair[2] - pair[1]
            # Don't ask.
            increment = CartesianIndex(map(i -> i == 0 ? 1 : div(i, maximum(map(abs, diff.I))), diff.I)...)
            for index in pair[1]:increment:pair[2]
                push!(barrierIndexes, index)
            end
        end
    end

    return barrierIndexes
end

function showState(barriers::Set{CartesianIndex}, sand::Set{CartesianIndex}, sandStart::CartesianIndex=CartesianIndex(500, 0))
    sandStart = CartesianIndex(500, 0)
    topleft = minimum([barriers..., sand..., sandStart])
    bottomright = maximum([barriers..., sand..., sandStart])

    for j in topleft.I[2]:bottomright.I[2]
        for i in topleft.I[1]:bottomright.I[1]
            ci = CartesianIndex(i, j)
            print(ci == sandStart ? '+' : ci in barriers ? '#' : ci in sand ? 'O' : '.')
        end
        println()
    end
end

function findingRestingState(
    barriers::Set{CartesianIndex},
    sand::Set{CartesianIndex};
    sandStart::CartesianIndex=CartesianIndex(500, 0),
    floorY::Union{Nothing, Int}=nothing,
)::Union{CartesianIndex, Nothing}
    lastBarrier = maximum(barriers)
    currentPos = sandStart

    if sandStart ∈ sand
        return nothing
    end


    belowOffset = CartesianIndex(0, +1)
    belowLeftOffset = CartesianIndex(-1, +1)
    belowRightOffset = CartesianIndex(+1, +1)

    while true
        below = currentPos + belowOffset
        belowLeft = currentPos + belowLeftOffset
        belowRight = currentPos + belowRightOffset

        if floorY === nothing && currentPos > lastBarrier
            return nothing
        end

        if floorY !== nothing
            if below[2] == floorY
                return currentPos
            end
        end

        if (below ∈ barriers || below ∈ sand) && (belowRight ∈ barriers || belowRight ∈ sand) && (belowLeft ∈ barriers || belowLeft ∈ sand)
            return currentPos
        end

        currentPos =
            (below ∉ barriers && below ∉ sand) ? below :
            (belowLeft ∉ barriers && belowLeft ∉ sand) ? belowLeft :
            belowRight
    end

    return nothing
end

barriers = processBarriers(loadBarriers("input.txt"))
part1sand = Set{CartesianIndex}()

while true
    result = findingRestingState(barriers, part1sand)
    if result === nothing
        break
    end
    push!(part1sand, result)
end

println("Part 1: ", length(part1sand))

part2sand = Set{CartesianIndex}()

while true
    result = findingRestingState(barriers, part2sand, floorY=(maximum(barriers) + CartesianIndex(0, 2))[2])
    if result === nothing
        break
    end
    push!(part2sand, result)
end

println("Part 2: ", length(part2sand))
