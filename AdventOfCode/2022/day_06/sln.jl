input = read(open("input.txt"), String)

using IterTools

function partitionSetSolution(input::String, partitionSize::Int)::Int
    for (i, partition) in enumerate(partition(input, partitionSize, 1))
        if length(Set(partition)) == partitionSize
            return i + (partitionSize - 1)
        end
    end

    return 0
end

function slidingWindowSolution(input::String, windowSize::Int)::Int
    slidingWindow = Dict{Char,Int}()
    for i in range(1, length(input))
        newestChar = input[i]
        slidingWindow[newestChar] = if haskey(slidingWindow, newestChar)
            slidingWindow[newestChar] + 1
        else
            1
        end

        if i > windowSize
            oldestChar = input[i - windowSize]
            if slidingWindow[oldestChar] == 1
                delete!(slidingWindow, oldestChar)
            else
                slidingWindow[oldestChar] -= 1
            end
        end

        if i >= windowSize
            if all(charCount -> charCount[2] <= 1, slidingWindow)
                return i
            end
        end
    end

    return -1
end

function slidingWindowSolution2(input::String, windowSize::Int)::Int
    slidingWindow = Dict{Char,Int}()
    for i in range(1, length(input))
        newestChar = input[i]
        slidingWindow[newestChar] = if haskey(slidingWindow, newestChar)
            slidingWindow[newestChar] + 1
        else
            1
        end

        if i >= windowSize
            if i > windowSize
                oldestChar = input[i - windowSize]
                if slidingWindow[oldestChar] == 1
                    delete!(slidingWindow, oldestChar)
                else
                    slidingWindow[oldestChar] -= 1
                end
            end

            if all(charCount -> charCount[2] <= 1, slidingWindow)
                return i
            end
        end
    end

    return -1
end

using BenchmarkTools

println()
println("Partition and Set Approach")
println("Part 1: ", @btime partitionSetSolution(input, 4))
println("Part 2: ", @btime partitionSetSolution(input, 14))

println()
println("Sliding-Window Approach")
println("Part 1: ", @btime slidingWindowSolution(input, 4))
println("Part 2: ", @btime slidingWindowSolution(input, 14))
