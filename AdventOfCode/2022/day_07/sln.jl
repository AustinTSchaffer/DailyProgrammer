struct DirEnt
    name::String
    isDir::Bool
    size::Int
end

struct ListCommand
end

struct CdCommand
    dirName::String
end

struct CommandAndResponse
    command::Union{ListCommand,CdCommand}
    output::Vector{DirEnt}
end

commandsAndResponses = Vector{CommandAndResponse}()
open("./input.txt", "r") do f
    cnr::Union{CommandAndResponse,Nothing} = nothing
    for line in eachline(f)
        if all(isspace, line)
            continue
        end

        if first(line) == '$'
            if cnr isa CommandAndResponse
                push!(commandsAndResponses, cnr)
            end

            cnr = CommandAndResponse(
                if startswith(line, "\$ cd")
                    CdCommand(last(split(line, " ")))
                else
                    ListCommand()
                end,
                []
            )
        elseif cnr isa CommandAndResponse
            dirent = split(line, " ")
            isDir = dirent[1] == "dir"
            size = isDir ? 0 : parse(Int, dirent[1])
            push!(cnr.output, DirEnt(
                dirent[2],
                isDir,
                size,
            ))
        end
    end

    push!(commandsAndResponses, cnr)
end

function calcCurrentDir(cwd::String, cdCommand::CdCommand)::String
    if cdCommand.dirName == "/"
        return "/"
    elseif cdCommand.dirName == ".."
        return cwd[1:(findlast('/', cwd) - 1)]
    elseif cwd == "/"
        return "/$(cdCommand.dirName)"
    else
        return "$(cwd)/$(cdCommand.dirName)"
    end
end

dirsListed = Set{String}()
dirSizes = Dict{String, Int}()
fileTree = Dict{String, Int}()
cwd = ""

for cnr in commandsAndResponses
    if cnr.command isa CdCommand
        global cwd = calcCurrentDir(cwd, cnr.command)
        if !haskey(dirSizes, cwd)
            dirSizes[cwd] = 0
        end
    elseif cnr.command isa ListCommand
        if !(cwd in dirsListed)
            push!(dirsListed, cwd)
            for dirEnt::DirEnt in cnr.output
                fileTree["$cwd/$(dirEnt.name)"] = dirEnt.size

                dirSizes["/"] += dirEnt.size
                if cwd != "/"
                    dirSizes[cwd] += dirEnt.size
                end
                for dirMarkerIndex in findall('/', cwd[2:length(cwd)])
                    dirSizes[cwd[1:dirMarkerIndex]] += dirEnt.size
                end
            end
        end
    else
        error("What is a $(cnr.command)?")
    end
end

println("Part 1: ", sum(
    x -> last(x),
    filter(
        x -> last(x) <= 100000,
        dirSizes
    )
))

fs_capacity = 70_000_000
fs_space_needed = 30_000_000
fs_space_used = dirSizes["/"]
space_to_free = fs_space_used - (fs_capacity - fs_space_needed)

println("Part 2: ", minimum(
    last,
    filter(
        x -> last(x) >= space_to_free,
        dirSizes
    )
))
