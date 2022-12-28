using Graphs

abstract type FlowGraphMetadata end

struct RectangleGraphMetadata <: FlowGraphMetadata
    input::String
    levelPackId::String
    collectionId::Int
    localLevelId::Int
    dims::Tuple{Int,Int}
end

struct FlowGraph
    graph::Graph
    flows::Vector{Vector{Int}}
    metadata::FlowGraphMetadata
end

function tryParseRectangleLevel(levelPackId::String, level::String, groups::AbstractVector)::Union{Nothing, FlowGraph}
    metadata = groups[1]

    graphDimensions::Tuple{Int,Int} = if ':' ∈ metadata[1]
        # Basic Rectangular
        width, height = map(i -> tryparse(Int, i), split(metadata[1], ':'))

        if width === nothing || height === nothing
            return nothing
        end

        (width, height)
    else
        # Basic Square?
        dims = tryparse(Int, metadata[1])

        if dims === nothing
            # Damn.
            return nothing
        end

        # Basic Square!
        (dims, dims)
    end

    numberOfFlows = parse(Int, metadata[4])
    flows = [
        map(i -> parse(Int, i), group)
        for group in groups[2:length(groups)]
    ]

    if numberOfFlows != length(flows)
        return nothing
    end

    graph = if length(metadata) == 4
        # Basic Rectangular Grid
        Graphs.grid(graphDimensions)
    elseif length(metadata) == 7
        # Special rules
        graph = Graphs.grid(graphDimensions)

        if !isempty(metadata[7])
            # Walls
            walls = map(w -> map(c -> parse(Int, c), split(w, '|')), split(metadata[7], ':'))
            for wall in walls
                rem_edge!(graph, wall[1] + 1, wall[2] + 1)
            end
        end

        graph
    else
        # ??
        return nothing
    end

    if graph === nothing
        return nothing
    end

    return FlowGraph(
        graph,
        flows,
        RectangleGraphMetadata(
            level,
            levelPackId,
            parse(Int, metadata[2]),
            parse(Int, metadata[3]),
            graphDimensions,
        ),
    )
end

function tryParseEncodedLevel(levelPackId::String, level::String)::Union{Nothing, FlowGraph}
    groups = [
        split(group, ',')
        for group in
        split(level, ';')
    ]

    try
        return tryParseRectangleLevel(levelPackId, level, groups)
    catch e
        println(stderr, "Caught exception: ", e)
        println(stderr, levelPackId, ":", level)
        return nothing
    end
end

function loadLevels(dir::String)::Tuple{Vector{FlowGraph}, Vector{String}}
    parsedGraphs = Vector{FlowGraph}()
    unparseable = Vector{String}()

    for filename in readdir(dir, join=true)
        file = open(filename, "r")

        for line in eachline(file)
            fg = tryParseEncodedLevel(basename(filename), line)
            if fg === nothing
                push!(unparseable, line)
            else
                push!(parsedGraphs, fg)
            end
        end

        close(file)
    end

    return parsedGraphs, unparseable
end

dir = "data/ffc_levels/all_levels/"
parsedGraphs, unparseable = loadLevels(dir)

println("Parsed Graphs: ", length(parsedGraphs))
println("Unparseable Graphs: ", length(unparseable))
