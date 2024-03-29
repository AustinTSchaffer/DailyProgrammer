struct Location
    coords::CartesianIndex
    height::Int8
    edges::Vector{CartesianIndex}
end

locations = Dict{CartesianIndex, Location}()
input = split(read(open("input.txt"), String), '\n', keepempty=false)

start::Union{Location, Nothing} = nothing
finish::Union{Location, Nothing} = nothing

for (i, row) in enumerate(input)
    for (j, val) in enumerate(row)
        idx = CartesianIndex(i, j)
        edges = Vector{CartesianIndex}()

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
        if haskey(locations, nidx) && locations[nidx].height <= location.height + 1
            push!(location.edges, nidx)
        end
    end
end

function reconstructPath(cameFrom::Dict{CartesianIndex, CartesianIndex}, current::CartesianIndex)::Vector{CartesianIndex}
    path = [current]
    while haskey(cameFrom, current)
        current = cameFrom[current]
        push!(path, current)
    end
    return path
end

euclidean = (a::CartesianIndex, b::CartesianIndex) -> sqrt(sum(map(z -> (z[2] - z[1])^2, zip(a.I, b.I))))
manhattan = (a::CartesianIndex, b::CartesianIndex) -> sum(map(z -> abs(z[2] - z[1]), zip(a.I, b.I)))

using DataStructures

function astar(locations::Dict{CartesianIndex, Location}, start::CartesianIndex; heuristic, foundgoal)
    exploredNodes = Set{CartesianIndex}()
    unexploredNodes = PriorityQueue{CartesianIndex, Float64}(Base.Order.Forward)
    cameFrom = Dict{CartesianIndex, CartesianIndex}()
    gScore = Dict{CartesianIndex, Int}()
    getGScore = (idx::CartesianIndex) -> haskey(gScore, idx) ? gScore[idx] : typemax(Int)
    fScore = Dict{CartesianIndex, Float64}()

    unexploredNodes[start] = fScore[start] = heuristic(start)
    gScore[start] = 0

    while !isempty(unexploredNodes)
        currentIdx::CartesianIndex = dequeue!(unexploredNodes)
        if foundgoal(currentIdx)
            return reconstructPath(cameFrom, currentIdx)
        end

        for neighborIdx in locations[currentIdx].edges
            tentativeGScore = gScore[currentIdx] + 1
            if tentativeGScore < getGScore(neighborIdx)
                cameFrom[neighborIdx] = currentIdx
                gScore[neighborIdx] = tentativeGScore
                unexploredNodes[neighborIdx] = fScore[neighborIdx] = tentativeGScore + heuristic(neighborIdx)
            end
        end

        push!(exploredNodes, currentIdx)
    end

    error("Path not found")
end

part1_result = astar(locations, start.coords, heuristic=currentIdx -> manhattan(currentIdx, finish.coords), foundgoal=currentIdx -> currentIdx == finish.coords)
for (i, row) in enumerate(input)
    for (j, val) in enumerate(row)
        if CartesianIndex(i, j) in part1_result
            printstyled(val, color=:red)
        else
            print(val)
        end
    end
    println()
end

println("Part 1: ", length(part1_result))

reverseLocations = Dict{CartesianIndex, Location}()
for (i, row) in enumerate(input)
    for (j, val) in enumerate(row)
        idx = CartesianIndex(i, j)
        edges = Vector{CartesianIndex}()

        val = val == 'S' ? 'a' : val == 'E' ? 'z' : val
        reverseLocations[idx] = Location(idx, Int8(val - 'a'), edges)
    end
end

for (idx, location) in reverseLocations
    for nidx in neighborIdxes
        nidx += idx
        if haskey(reverseLocations, nidx) && location.height <= reverseLocations[nidx].height + 1
            push!(location.edges, nidx)
        end
    end
end

println()

part2_result = astar(reverseLocations, finish.coords, heuristic=_ -> 0, foundgoal=currentIdx -> reverseLocations[currentIdx].height == 0)
for (i, row) in enumerate(input)
    for (j, val) in enumerate(row)
        if CartesianIndex(i, j) in part2_result
            printstyled(val, color=:red)
        else
            print(val)
        end
    end
    println()
end

println("Part 2: ", length(part2_result))
