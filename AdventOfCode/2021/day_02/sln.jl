struct Instruction
    direction::String
    distance::Int
end

mutable struct Location
    horizontal::Int
    vertical::Int
end

commands::Array{Instruction} = []
open("./input.txt", "r") do f
    for line in eachline(f)
        command, distance = split(line)
        push!(commands, Instruction(command, parse(Int, distance)))
    end
end

loc = Location(0, 0)
for command_idx in eachindex(commands)
    command::Instruction = commands[command_idx]
    if command.direction == "forward"
        loc.horizontal += command.distance
    end

    if command.direction == "up"
        loc.vertical += command.distance
    end

    if command.direction == "down"
        loc.vertical -= command.distance
    end
end

println(loc)
