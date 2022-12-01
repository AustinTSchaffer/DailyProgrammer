data::Array{Int} = []
open("./input.txt", "r") do f
    for line in eachline(f)
        append!(data, parse(Int, line))
    end
end

using IterTools

function part1(data::Array{Int})::Int
    higher = 0
    for pair in partition(data, 2, 1)
        if pair[2] > pair[1]
            higher += 1
        end
    end

    return higher
end

function part2(data::Array{Int})::Int
    higher = 0

    for windows in partition(partition(data, 3, 1), 2, 1)
        if sum(windows[2]) > sum(windows[1])
            higher += 1
        end
    end

    return higher
end

println(part1(data))
println(part2(data))
