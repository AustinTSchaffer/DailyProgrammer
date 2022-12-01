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
        sort!(maximums)
        deleteat!(maximums, 1)
    end

    return sum(maximums)
end

function part2_old(elves::Array{Array{Int}})::Int
    elves = map(sum, elves)
    elves = sort(elves, rev=true)
    return elves[1] + elves[2] + elves[3]
end

using BenchmarkTools

print("Part 1: ")
println(@btime part1(elves))
print("Part 2 (minimized sorting): ")
println(@btime part2(elves))
print("Part 2 (full sort): ")
println(@btime part2_old(elves))
