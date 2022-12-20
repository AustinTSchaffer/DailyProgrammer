shapes::Vector{Vector{Tuple{Int, Int}}} = [
    [
        (0, 0), (1, 0), (2, 0), (3, 0)
    ],
    [
                (1, 2),
        (0, 1), (1, 1), (2, 1),
                (1, 0),
    ],
    [
                        (2, 2),
                        (2, 1),
        (0, 0), (1, 0), (2, 0),
    ],
    [
        (0, 0), (0, 1), (0, 2), (0, 3)
    ],
    [
        (0, 1), (1, 1),
        (0, 0), (1, 0),
    ],
]

function getNthShape(shapes::Vector{Vector{Tuple{Int, Int}}}, iter::Int)::Vector{Tuple{Int, Int}}
    return shapes[((iter - 1) % length(shapes)) + 1]
end

function loadWind(filename::String)::Vector{Int}
    data = filter(c -> c != 0, map(c -> c == '>' ? 1 : c == '<' ? -1 : 0, collect(read(open(filename), String))))
end

function applyWind(shape::Vector{Tuple{Int, Int}}, windDirection::Int)::Vector{Tuple{Int, Int}}
    return return [
        (idx[1] + windDirection, idx[2])
        for idx in shape
    ]
end

function collision(shape::Vector{Tuple{Int, Int}}, rockPile::Set{Tuple{Int, Int}}, chamberWidth=7)::Bool
    return any(idx -> idx[1] <= 0 || idx[1] >= chamberWidth + 1, shape) || any(idx -> idx ∈ rockPile, shape)
end

gravityOffset = CartesianIndex(0, -1)

function simulateShape!(
    rockPile::Set{Tuple{Int, Int}},
    highestRock::Int,
    shapes::Vector{Vector{Tuple{Int, Int}}},
    shapeIndex::Int,
    wind::Vector{Int},
    windex::Int)::Tuple{Int, Int}

    shape = map(r -> (r[1] + 3, r[2] + highestRock + 4), getNthShape(shapes, shapeIndex))

    while true
        movedShape = applyWind(shape, wind[((windex - 1) % length(wind)) + 1])
        windex += 1
        shape = collision(movedShape, rockPile) ? shape : movedShape
        movedShape = map(idx -> (idx[1], idx[2] - 1), shape)

        if collision(movedShape, rockPile)
            for idx in shape
                push!(rockPile, idx)
            end

            for idx in shape
                if idx[2] > highestRock
                    highestRock = idx[2]
                end
            end

            break
        end

        shape = movedShape
    end

    if shapeIndex % 1_000_000 == 0
        print("Iteration: $shapeIndex. Pile size: $(length(rockPile)). ")
    end

    if shapeIndex % 1000 == 0
        for rock in rockPile
            if (highestRock - rock[2]) >= 1_000
                delete!(rockPile, rock)
            end
        end
    end

    if shapeIndex % 1_000_000 == 0
        println("New pile size: $(length(rockPile)). Highest rock: $(highestRock)")
    end

    return windex, highestRock
end

function printRockPile(rockPile::Set{CartesianIndex}, highestRock::CartesianIndex)
    for yIndex in highestRock[2]:-1:0
        for xIndex in 0:8
            if CartesianIndex(xIndex, yIndex) ∈ rockPile
                print('#')
            else
                print('.')
            end
        end
        println()
    end
    println()
end

wind = loadWind("input.txt")
sampleWind = loadWind("sample_input.txt")

rockPile = Set{Tuple{Int, Int}}()
for i in 1:7
    push!(rockPile, (i, 0))
end

windex = 1
highestRock = 0

for shapeIndex in 1:1_000_000_000_000
    result = simulateShape!(
        rockPile,
        highestRock,
        shapes,
        shapeIndex,
        wind,
        windex
    )

    global windex = result[1]
    global highestRock = result[2]
end

@show highestRock
