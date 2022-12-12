struct Location
    coords::CartesianIndex
    height::Int8
    edges::Vector{Location}
end

locations = Dict{CartesianIndex, Location}()
input = split(read(open("input.txt"), String), '\n', keepempty=false)

start::Union{Location, Nothing} = nothing
finish::Union{Location, Nothing} = nothing

for (i, row) in enumerate(input)
    for (j, val) in enumerate(row)
        idx = CartesianIndex(i, j)
        edges = Vector{Location}()

        locations[idx] = if val == 'S'
            val = 'a'
            global start = Location(idx, Int8(val - 'a'), edges)
        elseif val == 'E'
            val = 'z'
            global finish = Location(idx, Int8(val - 'a'), edges)
        else
            Location(idx, Int8(val - 'a'), edges)
        end
    end
end

if isnothing(start) || isnothing(finish)
    error("Start and/or End not found")
end

neighborIdxes = map(CartesianIndex, [
    (+1, 0),
    (-1, 0),
    (0, +1),
    (0, -1),
])

for (idx, location) in locations
    for nidx in neighborIdxes
        nidx += idx
        isHeightAdjacentNeighbor = (
            haskey(locations, nidx) && (
                locations[nidx].height == location.height ||
                locations[nidx].height == location.height + 1
            )
        )
        if isHeightAdjacentNeighbor
            push!(location.edges, locations[nidx])
        end
    end
end

# TODO: A* search

