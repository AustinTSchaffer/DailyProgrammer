struct Valve
    id::String
    flowRate::Int
    adjValves::Vector{String}
end

struct State
    turnsRemaining::Int
    position::String
    prevPosition::Union{String, Nothing}
    openedValves::Vector{String}
    pressureDelta::Int
    releasedPressure::Int
end

struct StateWithElephant
    turnsRemaining::Int
    position::String
    prevPosition::Union{String, Nothing}
    elephantPosition::Union{String, Nothing}
    elephantPrevPosition::Union{String, Nothing}
    openedValves::Vector{String}
    pressureDelta::Int
    releasedPressure::Int
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

function part1(input::Dict{String, Valve}, state::State)::State
    function _part1(state::State)::Vector{State}
        if state.turnsRemaining == 0
            return [state]
        end

        newReleasedPressure = state.releasedPressure + state.pressureDelta
        turnsRemaining = state.turnsRemaining - 1

        # println(state)

        bestOutcome = newReleasedPressure
        bestOutcomes = Vector{State}()

        if !(state.position in state.openedValves) && (input[state.position].flowRate > 0)
            newState = State(
                turnsRemaining,
                state.position,
                nothing,
                [state.openedValves..., state.position],
                state.pressureDelta + input[state.position].flowRate,
                newReleasedPressure,
            )

            for outcome in _part1(newState)
                if outcome.releasedPressure > bestOutcome
                    bestOutcome = outcome.releasedPressure
                    bestOutcomes = [outcome]
                elseif outcome.releasedPressure == bestOutcome
                    push!(bestOutcomes, outcome)
                end
            end
        end

        for neighbor in input[state.position].adjValves
            if neighbor == state.prevPosition
                continue
            end

            newState = State(
                turnsRemaining,
                neighbor,
                state.position,
                state.openedValves,
                state.pressureDelta,
                newReleasedPressure,
            )

            for outcome in _part1(newState)
                if outcome.releasedPressure > bestOutcome
                    bestOutcome = outcome.releasedPressure
                    bestOutcomes = [outcome]
                elseif outcome.releasedPressure == bestOutcome
                    push!(bestOutcomes, outcome)
                end
            end
        end

        if length(bestOutcomes) == 0
            return [State(
                turnsRemaining,
                state.position,
                state.position,
                state.openedValves,
                state.pressureDelta,
                newReleasedPressure,
            )]
        end

        return bestOutcomes
    end

    return _part1(state)[1]
end

# function part2(input::Dict{String, Valve}, state::StateWithElephant)::StateWithElephant
#     function _part2(state::StateWithElephant)::Vector{StateWithElephant}
#         if state.turnsRemaining == 0
#             return [state]
#         end

#         newReleasedPressure = state.releasedPressure + state.pressureDelta
#         turnsRemaining = state.turnsRemaining - 1

#         # println(state)

#         bestOutcome = newReleasedPressure
#         bestOutcomes = Vector{StateWithElephant}()

#         if !(state.position in state.openedValves) && (input[state.position].flowRate > 0)
#             newState = StateWithElephant(
#                 turnsRemaining,
#                 state.position,
#                 nothing,
#                 [state.openedValves..., state.position],
#                 state.pressureDelta + input[state.position].flowRate,
#                 newReleasedPressure,
#             )

#             for outcome in _part1(newState)
#                 if outcome.releasedPressure > bestOutcome
#                     bestOutcome = outcome.releasedPressure
#                     bestOutcomes = [outcome]
#                 elseif outcome.releasedPressure == bestOutcome
#                     push!(bestOutcomes, outcome)
#                 end
#             end
#         end

#         for neighbor in input[state.position].adjValves
#             if neighbor == state.prevPosition
#                 continue
#             end

#             newState = StateWithElephant(
#                 turnsRemaining,
#                 neighbor,
#                 state.position,
#                 state.openedValves,
#                 state.pressureDelta,
#                 newReleasedPressure,
#             )

#             for outcome in _part1(newState)
#                 if outcome.releasedPressure > bestOutcome
#                     bestOutcome = outcome.releasedPressure
#                     bestOutcomes = [outcome]
#                 elseif outcome.releasedPressure == bestOutcome
#                     push!(bestOutcomes, outcome)
#                 end
#             end
#         end

#         if length(bestOutcomes) == 0
#             return [StateWithElephant(
#                 turnsRemaining,
#                 state.position,
#                 state.position,
#                 state.openedValves,
#                 state.pressureDelta,
#                 newReleasedPressure,
#             )]
#         end

#         return bestOutcomes
#     end

#     return _part2(state)[1]
# end

println("Part 1: ", part1(input, State(30, "AA", nothing, Vector{String}(), 0, 0)).releasedPressure)

# println("Part 2: ", part2(input, StateWithElephant(26, "AA", nothing, "AA", nothing, Vector{String}(), 0, 0)).releasedPressure)
