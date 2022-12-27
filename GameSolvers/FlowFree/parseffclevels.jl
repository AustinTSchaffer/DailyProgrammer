using Graphs

struct FlowGraph
    input::String
    dims::Tuple{Int,Int}
    collectionId::Int
    localLevelId::Int
    flows::Vector{Vector{Int}}
    graph::Graph
end

function tryParseEncodedLevel(level::String)::Union{Nothing, FlowGraph}
    groups = [
        split(group, ',')
        for group in
        split(level, ';')
    ]

    metadata = groups[1]

    if length(metadata) != 4
        return nothing
    end

    try
        numberOfFlows = parse(Int, metadata[4])
        flows = [
            map(i -> parse(Int, i), group)
            for group in groups[2:length(groups)]
        ]

        if numberOfFlows != length(flows)
            return nothing
        end

        graphDimensions::Tuple{Int,Int} = if ':' ∈ metadata[1]
            # Basic Rectangular
            width, height = map(i -> parse(Int, i), split(metadata[1], ':'))
            (width, height)
        else
            # Basic Square?
            dims = tryparse(Int, metadata[1])

            if dims === nothing
                return nothing
            end

            # Basic Square!
            (dims, dims)
        end

        graph = Graphs.grid(graphDimensions)

        return FlowGraph(
            level,
            graphDimensions,
            parse(Int, metadata[2]),
            parse(Int, metadata[3]),
            flows,
            graph
        )
    catch e
        println(stderr, "Caught exception", e)
        println(stderr, level)
        return nothing
    end
end

function loadLevels(dir::String)::Tuple{Vector{FlowGraph}, Vector{String}}
    parsedGraphs = Vector{FlowGraph}()
    unparseable = Vector{String}()

    for filename in readdir(dir, join=true)
        file = open(filename, "r")

        for line in eachline(file)
            fg = tryParseEncodedLevel(line)
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
