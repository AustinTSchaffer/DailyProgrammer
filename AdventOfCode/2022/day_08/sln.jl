input = split(read(open("input.txt"), String), '\n', keepempty=false)

height = length(input)
width = length(input[1])

trees = Array{Int8}(undef, height, width)

for (i, row) in enumerate(input)
    for (j, val) in enumerate(row)
        trees[i, j] = Int8(val - '0')
    end
end

visibleTrees = Vector{CartesianIndex}()
for idx in CartesianIndices(trees)
    # down?
    if all(y -> trees[y, idx[2]] < trees[idx], (idx[1]+1):height)
        push!(visibleTrees, idx)
    # up?
    elseif all(y -> trees[y, idx[2]] < trees[idx], (idx[1]-1):-1:1)
        push!(visibleTrees, idx)
    # right?
    elseif all(x -> trees[idx[1], x] < trees[idx], (idx[2]+1):width)
        push!(visibleTrees, idx)
    # left?
    elseif all(x -> trees[idx[1], x] < trees[idx], (idx[2]-1):-1:1)
        push!(visibleTrees, idx)
    end
end

println("Part 1: ", length(visibleTrees))

function scenicScore(idx::CartesianIndex, trees::Matrix{Int8})::Int
    totalScore = 1
    height, width = size(trees)

    downScore = 0
    for downIdx in (idx[1]+1):height
        downScore += 1
        if trees[downIdx, idx[2]] >= trees[idx]
            break
        end
    end
    totalScore *= downScore

    upScore = 0
    for upIdx in (idx[1]-1):-1:1
        upScore += 1
        if trees[upIdx, idx[2]] >= trees[idx]
            break
        end
    end
    totalScore *= upScore

    leftScore = 0
    for leftIdx in (idx[2]-1):-1:1
        leftScore += 1
        if trees[idx[1], leftIdx] >= trees[idx]
            break
        end
    end
    totalScore *= leftScore

    rightScore = 0
    for rightIdx in (idx[2]+1):width
        rightScore += 1
        if trees[idx[1], rightIdx] >= trees[idx]
            break
        end
    end
    totalScore *= rightScore

    return totalScore
end

# sample_trees = [
#     3 0 3 7 3;
#     2 5 5 1 2;
#     6 5 3 3 2;
#     3 3 5 4 9;
#     3 5 3 9 0;
# ]

println("Part 2: ", maximum(idx -> scenicScore(idx, trees), CartesianIndices(trees)))
