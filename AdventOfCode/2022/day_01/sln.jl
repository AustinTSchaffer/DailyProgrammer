elves::Array{Array{Int}} = []

open("./input.txt", "r") do f
    calories::Array{Int} = []
    for line in eachline(f)
        if isempty(line)
            push!(elves, calories)
            calories = []
        else
            push!(calories, parse(Int, line))
        end
    end

    push!(elves, calories)
end

function part1(elves::Array{Array{Int}})::Int
    return maximum(sum, elves)
end

function part2(elves::Array{Array{Int}})::Int
    maximums = [0, 0, 0]
    for elf in elves
        push!(maximums, sum(elf))
        maximums = sort(maximums)
        deleteat!(maximums, 1)
    end

    return sum(maximums)
end

println(part1(elves))
println(part2(elves))
