input = split(read(open("input.txt"), String), '\n', keepempty=false)

height = length(input)
width = length(input[1])

trees = Array{Int8}(undef, height, width)

for (i, row) in enumerate(input)
    for (j, val) in enumerate(row)
        printstyled(val; color=div(255, (Int(val - '0') + 1)))
        print(' ')
    end
    println()
end


