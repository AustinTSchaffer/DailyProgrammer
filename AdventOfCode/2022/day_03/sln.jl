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

# Split each string in half. The map(identity, ...) is to convert
# the halved string back to an array. Iterators.map is used here
# to create a lazy stream as opposed to creating a new list for
# every step in the chain.
part1 = Iterators.map(elf -> map(identity, partition(elf, div(length(elf), 2))), data)

# Find the intersection of each compartment.
# Add up the sum of the scores of the letters for part 1
part1 = sum(
    scoreLetter(letter)
    for compartment in part1
    for intersection in intersect(compartment[1], compartment[2])
    for letter in intersection
)

println("Part 1: ", part1)

# Partition the elves into trios, in order, defining the elves' groups
# Determine the badge ID for each elf group
# Sum up the badge scores
part2 = sum(
    scoreLetter(badge)
    for group in partition(data, 3)
    for badge in intersect(group[1], group[2], group[3])
)

println("Part 2: ", part2)
