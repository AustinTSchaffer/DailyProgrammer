-- @file        AlienInvasionInversion.lua
-- @version     1.0 
-- @author      Austin Schaffer 
-- @since       2016-06-20 
-- @revision    2016-06-21 
-- @see ./README.md


local function _readFile(filename)
    -- Reads in a file that has been formatted according to the input specified
    -- by the README. Local function that is only visible to members of this 
    -- file.
    -- 
    -- @param filename Path and name of formatted text file to load
    -- 
    -- @return Returns 2 values 
    --      1 = n,   number,   length of one side of the square map from file
    --      2 = map, 2D table, indexed [1-N][1-N], contains map data from file
    
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


local function _expandSquare(N, map, iLoc, jLoc, D)

    -- Recursive helper function. Searches a square located at (iLoc, jLoc)
    -- with dimension D. If no rocky acres are found, D is incremented and the
    -- function is called again. Search ends when a rocky acre is found within
    -- a search square of size D, located at (iLoc, jLoc). Outputs the final 
    -- value of D along with a delta value, referring to the location of the
    -- east-most rocky acre, allowing the search to eliminate some future
    -- search squares.
    -- 
    -- More details can be found in ./README.md
    --
    -- @param N    Numerical dimension of one side of the square map.
    -- @param map  2D table, loaded from file.
    -- @param iLoc row# of the north-west most acre of this search square.
    -- @param jLoc col# of the north-west most acre of this search square.
    -- @param D    Starting dimension of one side of the search square.
    --
    -- @return Returns a pair of values
    --      1 = D,      number, the final expanded dimension of a search square
    --          at (iLoc, jLoc) that contains at least one acre of rocks.
    --      2 = jDelta, number, represents how many acres eastward (+j) the 
    --          next search area should start, based on the eastmost acre of
    --          rocks found in the largest expansion of a search
    --
    -- number, table, number, number, number --> number, number

    local suitable = true
    local jDelta = 1

    if ((iLoc + D - 1) > N) then suitable = false end
    if ((jLoc + D - 1) > N) then suitable = false end

    if not suitable then return D, jDelta end

    for i=1, D do
        for j=1, D do
            if map[iLoc + i - 1][jLoc + j - 1] == "X" then
                suitable = false
                if j > jDelta then jDelta = j end
            end
        end
    end
    
    if suitable then 
        D, jDelta = _expandSquare(N, map, iLoc, jLoc, D + 1)
    end

    return D, jDelta
end


local function _printMap(map)
    -- Utilitiy function that prints a 2D table to stdout.
    -- 
    -- @param map 2D table to print.
    -- @return Does not return any values.

    for i=1, #map do
        local line = ""
        for j=1, #map[i] do
            line = line .. map[i][j]
        end
        print(line)
    end
end


function invade(filename)
    -- Entrypoint to module functionality. Finds the largest square area
    -- that can be turned into a landing zone based on a map of the area
    -- that distinguishes acres of crops from acres of rocks.
    --
    -- See ./README.md for more details.
    --
    -- @param filename Name and path to a text file that contains a properly
    -- formatted description of the area to invade.
    -- 
    -- @return Returns a string, formatted to tell the user where they should
    -- invade and the dimensions of the landing area.

    local N, map = _readFile(filename)
    local D, jDelta, iPrime, jPrime = 1, 1, 0, 0

    -- While loops were used here, since for loops are very restricting
    local i = 1
    while (i <= (N + 1 - D)) do
        local j = 1
        while (j <= (N + 1 - D)) do

            newD, jDelta = _expandSquare(N, map, i, j, D)

            if newD > D then
                D = newD
                iPrime = i
                jPrime = j
            end

            j = j + jDelta
        end
        i = i + 1
    end

    return (D-1).."x"..(D-1).." square at i="..(iPrime-1).." and j="..(jPrime-1)
end
