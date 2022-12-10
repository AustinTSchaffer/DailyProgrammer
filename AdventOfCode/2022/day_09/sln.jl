struct Move
    orig::String
    direction::CartesianIndex
    distance::Int
end

function parseMoves(data::Vector{String})::Vector{Move}
    return map(
        line -> begin
            s = split(line, ' ')
            dir = CartesianIndex(
                s[1] == "U" ? (1, 0) :
                s[1] == "D" ? (-1, 0) :
                s[1] == "L" ? (0, -1) :
                s[1] == "R" ? (0, 1) :
                error("Unknown instruction $line")
            )
            Move(line, dir, parse(Int, s[2]))
        end,
        data
    )
end

moves = parseMoves(readlines(open("input.txt")))
sampleMoves = parseMoves([
    "R 4"
    "U 4"
    "L 3"
    "D 1"
    "R 4"
    "D 1"
    "L 5"
    "R 2"
])
largerSampleMoves = parseMoves([
    "R 5"
    "U 8"
    "L 8"
    "D 3"
    "R 17"
    "D 10"
    "L 25"
    "U 20"
])

function move!(move::Move, head::CartesianIndex, tail::CartesianIndex, tailLocations::Set{CartesianIndex})::Tuple{CartesianIndex, CartesianIndex}    
    for i = range(1, move.distance)
        oldhead = head
        head = head + move.direction
        diff = head - tail

        if maximum(map(abs, diff.I)) > 1
            tail = oldhead
        end

        push!(tailLocations, tail)
    end

    return (head, tail)
end

function move!(move::Move, rope::Vector{CartesianIndex}, tailLocations::Set{CartesianIndex})::Vector{CartesianIndex}
    for i = range(1, move.distance)
        movements = Vector{CartesianIndex}()
        newrope = Vector{CartesianIndex}()
        push!(movements, move.direction)
        push!(newrope, rope[1] + move.direction)

        for (prevIndex, curr) in enumerate(rope[2:length(rope)])
            diff = newrope[prevIndex] - curr
            absDiff = map(abs, diff.I)
            newCurr = if maximum(absDiff) > 1
                if absDiff == (0, 2) || absDiff == (2, 0)
                    CartesianIndex(
                        curr[1] + div(diff[1], 2),
                        curr[2] + div(diff[2], 2),
                    )
                elseif map(abs, movements[prevIndex].I) == (1, 1)
                    curr + movements[prevIndex]
                else
                    rope[prevIndex]
                end
            else
                curr
            end

            push!(newrope, newCurr)
            push!(movements, newCurr - curr)
        end

        rope = newrope
        push!(tailLocations, last(rope))
    end

    return rope
end

tailLocations = Set{CartesianIndex}([CartesianIndex(0, 0)])
state = (
    CartesianIndex(0, 0),
    CartesianIndex(0, 0),
)

for move in moves
    global state = move!(move, state[1], state[2], tailLocations)
end

println("Part 1: ", length(tailLocations))

tailLocations = Set{CartesianIndex}([CartesianIndex(0, 0)])
part2state::Vector{CartesianIndex} = [
    CartesianIndex(0, 0), # H
    CartesianIndex(0, 0), # 1
    CartesianIndex(0, 0), # 2
    CartesianIndex(0, 0), # 3
    CartesianIndex(0, 0), # 4
    CartesianIndex(0, 0), # 5
    CartesianIndex(0, 0), # 6
    CartesianIndex(0, 0), # 7
    CartesianIndex(0, 0), # 8
    CartesianIndex(0, 0), # 9
]

for move in moves
    global part2state = move!(move, part2state, tailLocations)
end

println("Part 2: ", length(tailLocations))
