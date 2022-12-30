using Graphs
using Plots
using GraphRecipes

struct GraphMetadata
    input::String
    levelPackId::String
    collectionId::Int
    localLevelId::Int
    dims::Tuple{Int,Int}
end

struct FlowGraph
    graph::Graph
    flows::Vector{Vector{Int}}
    metadata::GraphMetadata
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
        GraphMetadata(
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

function loadLevels(dir::String)
    parsedGraphs = Vector{FlowGraph}()
    parsedGraphsDict = Dict{String, Vector{FlowGraph}}()

    unparseable = Vector{String}()
    unparseableDict = Dict{String, Vector{String}}()

    for filepath in readdir(dir, join=true)
        file = open(filepath, "r")
        filename = basename(filepath)

        parsedGraphsDict[filename] = []
        unparseableDict[filename] = []

        for line in eachline(file)
            fg = tryParseEncodedLevel(filename, line)
            if fg === nothing
                push!(unparseable, line)
                push!(unparseableDict[filename], line)
            else
                push!(parsedGraphs, fg)
                push!(parsedGraphsDict[filename], fg)
            end
        end

        close(file)
    end

    return parsedGraphs, parsedGraphsDict, unparseable, unparseableDict
end

emptyCellColor = :gray

flowColors = map(c -> Colors.RGBA(map(i -> i/255, c)...), (
    (205,74,52), # Red
    (87,136,57), # Green
    (58,44,234), # Blue
    (226,223,100), # Yellow
    (215,147,73),  # Orange
    (164,247,251), # Cyan
    (208,76,188), # Magenta
    (158,247,103), # Lime Green
    (134,63,55), # Burnt Red
    (150,139,95), # Olive
    (219,137,224), # Pink
    (105,37,119), # Purple
    (38,30,146), # Dark Blue
    (255,255,255), # White
    (82,123,125), # Dark Cyan
    (159,158,183), # Gray
))

function flowGraphPlot(flowGraph::FlowGraph; palette=flowColors, emptyCellColor=emptyCellColor, size=(1000,1000), fontsize=2.0, nodesize=1.0, showSolution=false)
    nodeGroupsToColor = showSolution ? flowGraph.flows : [(first(f), last(f)) for f in flowGraph.flows]
    vertexIndices = 1:Graphs.nv(flowGraph.graph)

    if length(nodeGroupsToColor) > length(palette)
        error("Not enough colors in the palette")
    end

    nodeColors = []

    for i in vertexIndices
        endfound = false
        for (j, v) in enumerate(nodeGroupsToColor)
            if (i-1) ∈ v
                endfound = true
                push!(nodeColors, palette[j])
                break
            end
        end

        if !endfound
            push!(nodeColors, emptyCellColor)
        end
    end

    return graphplot(flowGraph.graph, names=0:(Graphs.nv(flowGraph.graph)-1), curves=false, nodeshape=:rect, fontsize=fontsize, nodesize=nodesize, mc=nodeColors, size=size)
end

# dir = "../data/ffc_levels/all_levels/"
# parsedGraphs, unparseable, parsedGraphsDict, unparseableDict = loadLevels(dir)

# println("Parsed Graphs: ", length(parsedGraphs))
# println("Unparseable Graphs: ", length(unparseable))
