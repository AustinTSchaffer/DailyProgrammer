data::Array{String} = []
open("./input.txt", "r") do f
    for line in eachline(f)
        if all(isspace, line)
            continue
        end

        push!(data, line)
    end
end

# Determines the score for a single character
scoreLetter(c::Char) = islowercase(c) ?
    c - 'a' + 1 :
    c - 'A' + 27

using IterTools

# Split each string in half
part1 = map(d -> map(identity, partition(d, div(length(d), 2))), data)

# Find the intersection for each pair of sets
part1 = map(e -> intersect(e[1], e[2]), part1)

# Add up the sum of the scores of the letters for part 1
part1 = sum(
    scoreLetter(letter)
    for intersection in part1
    for letter in intersection
)

println("Part 1: ", part1)

# Partition the elves into trios, in order, defining the elves' groups
part2 = partition(data, 3)

# Determine the badge ID for each elf group
part2 = [
    intersect(group[1], group[2], group[3])
    for group in part2
]

# Sum up the badge scores
part2 = sum(
    scoreLetter(badge)
    for group in part2
    for badge in group
)

println("Part 2: ", part2)
