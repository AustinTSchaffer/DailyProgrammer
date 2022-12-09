input = split(read(open("input.txt"), String), '\n')

trees = map(
    row -> map(
        val -> convert(Int, val),
        row
    ),
    input
)

@show trees
