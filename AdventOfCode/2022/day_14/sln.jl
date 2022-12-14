input = split(read(open("input.txt"), String), '\n', keepempty=false)

barriers = Vector{Vector{CartesianIndex}}()
for line in input
    barrier = Vector{CartesianIndex}()
    push!(barriers, barrier)
    x = split(line, " -> ")
    for _x in x
        push!(barrier, CartesianIndex(map(i -> parse(Int, i), split(_x, ','))...))
    end
end

using IterTools

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

sandStart = CartesianIndex(500, 0)
topleft = minimum([barrierIndexes..., sandStart])
bottomright = maximum([barrierIndexes..., sandStart])

for j in topleft.I[2]:bottomright.I[2]
    for i in topleft.I[1]:bottomright.I[1]
        ci = CartesianIndex(i, j)
        print(ci == sandStart ? '+' : ci in barrierIndexes ? '#' : '.')
    end
    println()
end
