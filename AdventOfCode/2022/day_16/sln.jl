struct Valve
    id::String
    flowRate::Int
    adjValves::Vector{String}
end

valveRegex = r"Valve (\w+) has flow rate=(\d+);.+valves? (.+)"

function loadInput(filename::String)::Dict{String, Valve}
    valves = Dict{String,Valve}()

    open(filename, "r") do f
        for line in readlines(f)
            sbMatch = match(valveRegex, line)
            
            id = sbMatch[1]
            rate = parse(Int, sbMatch[2])
            adj = collect(split(sbMatch[3], ", "))

            valves[id] = Valve(id, rate, adj)
        end
    end

    return valves
end

input = loadInput("input.txt")
sampleInput = loadInput("sample_input.txt")

for node in input
    for edge in node[2].adjValves
        println("$(node[2].id):$(node[2].flowRate) $(input[edge].id):$(input[edge].flowRate)")
    end
end
