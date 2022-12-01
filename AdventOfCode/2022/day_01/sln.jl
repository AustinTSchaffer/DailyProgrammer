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
end

function part1(elves::Array{Array{Int}})::Int
    return maximum(sum, elves)
end

function part2(elves::Array{Array{Int}})::Int
    elves = map(sum, elves)
    elves = sort(elves, rev=true)
    return elves[1] + elves[2] + elves[3]
end

println(part1(elves))
println(part2(elves))
