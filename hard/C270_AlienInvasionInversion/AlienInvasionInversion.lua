function invade(filename)
    
    local N, map = _readFile(filename)
    local D, jDelta, iPrime, jPrime = 1, 1, 0, 0

    -- Anonymous function for loop conditions
    function minus(n,d) return n - d end

    for i = 1, minus(N+1,D), 1 do
        for j = 1, minus(N+1,D), jDelta do

            newD, jDelta = _expandSquare(N, map, i, j, D)
            
            if newD > D then
                D = newD
                iPrime = i
                jPrime = j
            end
        end
    end

    return (D-1).."x"..(D-1).." square at i="..(iPrime-1).." and j="..(jPrime-1)
end


function _readFile(filename)

    local file = io.open(filename)
    
    local n = tonumber(file:read())
    local map = {}
    
    for line in file:lines() do
         mapLine = {}
         line:gsub(".", function(c) table.insert(mapLine,c) end)
         table.insert(map, mapLine)
     end

    file:close()

    return n, map
end

function _expandSquare(N, map, iLoc, jLoc, D)
    
    local suitable = true
    local jDelta = 1

    if ((iLoc + D - 1) > N) then suitable = false end
    if ((jLoc + D - 1) > N) then suitable = false end

    if not suitable then return D, jDelta end

    for i=1, D do
        for j=1, D do
            if map[iLoc + i - 1][jLoc + j - 1] == "X" then
                suitable = false
                if j > jLoc then jDelta = j end
            end
        end
    end
    
    if suitable then 
        D, jDelta = _expandSquare(N, map, iLoc, jLoc, D + 1)
    end

    return D, jDelta
end


function printMap(map)
    for i=1, #map do
        local line = ""
        for j=1, #map[i] do
            line = line .. map[i][j]
        end
        print(line)
    end
end
