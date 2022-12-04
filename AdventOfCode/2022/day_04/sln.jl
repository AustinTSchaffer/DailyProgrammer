assignmentPairs::Array{Tuple{UnitRange, UnitRange}} = []
open("./input.txt", "r") do f
    for line in eachline(f)
        if all(isspace, line)
            continue
        end

        assignments = split(line, ',')
        assignments = map(a -> map(sa -> parse(Int, sa), split(a, '-')), assignments)
        push!(assignmentPairs, (
            assignments[1][1]:assignments[1][2],
            assignments[2][1]:assignments[2][2],
        ))
    end
end

part1 = 0
for pair in assignmentPairs
    union = range(
        min(
            first(pair[1]),
            first(pair[2])
        ),
        max(
            last(pair[1]),
            last(pair[2])
        )
    )

    if in(union, pair)
        global part1 += 1
    end
end
println("Part 1: ", part1)

part2 = sum(
    pair -> length(intersect(pair[1], pair[2])) > 0,
    assignmentPairs
)
println("Part 2: ", part2)
