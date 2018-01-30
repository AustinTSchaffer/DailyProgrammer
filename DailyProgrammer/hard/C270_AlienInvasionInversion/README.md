# Challenge #270 [Hard] Alien Invasion Inversion

After millennia of tiresome searching, we finally discovered alien life on Planet Yert, and Earth unanimously decided to invade because the Yertlings were a menace to galactic peace having finally achieved the bronze age. In preparation for our space marine invasion, a scouting drone needs to carve out a huge crop square in a field. The only problem is that our drone can't cut through some mysterious rock-like material scattered throughout the realm.

### Input

The first line is N, which refers to the size of the N by N square map. The next N lines will have N characters each. A '-' represents an acre of crops and an 'X' represents an acre of indestructible, uneven rocks.

Example:

    8
    --X----X
    -----X--
    X--X----
    --X-----
    X--X----
    XXXX----
    --X-----
    --X---X-

### Output

Determine the largest square of crops that our drone can cut in preparation for our invasion. For each acre of crops that we can mow down in the square, we can invade with one dropship. Find the largest square not containing any rocks and display the number of dropships we can dispatch. In the above example, the output would be "16 dropships!". Below, the optimal square is marked with O's:

    --X----X
    -----X--
    X--XOOOO
    --X-OOOO
    X--XOOOO
    XXXXOOOO
    --X-----
    --X---X-

### Examples

Test files have been included under the /data/ subdirectory. These files are listed below, along with their respective solutions.

    Environment5.txt   // Solution = 9 acres
    Environment8.txt   // Solution = 16 acres
    Environment50.txt  // Solution = 49 acres
    Environment100.txt // Solution = 81 acres

### Implementation

The solution was implemented as a Lua command line program. This was an exercise that included learning file IO and 2D array operations.

The program determines the largest acceptable square of land by iterating an expanding square through the map. This iterating square starts in the top left corner with a size of 1. At each iteration, a square of size D, with its top-left corner located at some i and j, will be checked for unsuitable terrain, following an out-of-bounds check. If no rocky acres are found, D will be incremented until it finds unsuitable terrain or the edge of the map.

Below is an example of an expanding square checking a few locations. The final D value for the square is 5, but the result is 4. The return value of the search is D - 1, because a square of sized D - 1 was the largest square that was found that did not have any rocky acres. Each row denotes a search and expand cycle, with the following row being the next search location. No steps are skipped in between row 1 and row 2. The square is incremented along the x-axis by 3, instead of 1, because the east-most rocky acre found in the previous search . The search performed in row 2 also found a 

    [-]- X - - - - X   [- -]X - - - - X   [- - X]- - - - X 
     - - - - - X - -   [- -]- - - X - -   [- - -]- - X - - 
     X - - X - - - -    X - - X - - - -   [X - -]X - - - - 
     - - X - - - - -    - - X - - - - -    - - X - - - - - 
     X - - X - - - -    X - - X - - - -    X - - X - - - - 
     X X X X - - - -    X X X X - - - -    X X X X - - - - 
     - - X - - - - -    - - X - - - - -    - - X - - - - - 
     - - X - - - X -    - - X - - - X -    - - X - - - X - 
     
     - - X[- - -]- X
     - - -[- - X]- -
     X - -[X - -]- -
     - - X - - - - -
     X - - X - - - -
     X X X X - - - -
     - - X - - - - -
     - - X - - - X -
     
     - - X - - -[- X B]
     - - - - - X[- - B]
     X - - X - -[- - B]
     - - X - - - - -
     X - - X - - - -
     X X X X - - - -
     - - X - - - - -
     - - X - - - X -


     - - X - - - - X
    [- - -]- - X - -
    [X - -]X - - - -
    [- - X]- - - - -
     X - - X - - - -
     X X X X - - - -
     - - X - - - - -
     - - X - - - X -
     
     ...
     
     - - X - - - - X    - - X - - - - X    - - X - - - - X
     - - - - - X - -    - - - - - X - -    - - - - - X - -
     X - - X[- - -]-    X - - X[- - - -]   X - - X[- - - - B]
     - - X -[- - -]-    - - X -[- - - -]   - - X -[- - - - B]
     X - - X[- - -]-    X - - X[- - - -]   X - - X[- - - - B]
     X X X X - - - -    X X X X[- - - -]   X X X X[- - - - B]
     - - X - - - - -    - - X - - - - -    - - X -[- - - - B]
     - - X - - - X -    - - X - - - X -    - - X - - - X -
     
     - - X - - - - X
     - - - - - X - -
     X - - X - - - -
    [- - X - -]- - -
    [X - - X -]- - -
    [X X X X -]- - -
    [- - X - -]- - -
    [- - X - -]- X -
     
     - - X - - - - X
     - - - - - X - -
     X - - X - - - -
     - - X -[- - - - B]
     X - - X[- - - - B]
     X X X X[- - - - B]
     - - X -[- - - - B]
     - - X -[- - X - B]

In rows 3, 5, and 7, B stands for _boundary_, referring to an expansion that pushed the search area outside the bounds of the map. Boundary detection is performed prior to a search, preventing out of bounds errors and reducing the total number of comparisons.

### Usage

This solution was implemented as a set of Lua functions that can be used in the console in intaractive mode. The _invade(filename)_ function outputs a string, showing the max square found along with the location of the top left corner of the square. All (i,j) pairs are normalized to start at (0,0), instead of Lua's default of (1,1), and refer to a row and a column, respectively. The output does not match the output description of the challenge in order to provide useful information to the user.

    > lua -i -e "dofile('AlienInvasionInversion.lua')"
    Lua 5.1.5  Copyright (C) 1994-2012 Lua.org, PUC-Rio
    
    > print(invade("data/Environment5.txt"))
    3x3 square at i=1 and j=0
    
    > print(invade("data/Environment8.txt"))
    4x4 square at i=2 and j=4
    
    > print(invade("data/Environment50.txt"))
    7x7 square at i=5 and j=14
    
    > print(invade("data/Environment100.txt"))
    9x9 square at i=10 and j=71
    
    > print(invade("data/Environment500.txt"))
    9x9 square at i=10 and j=71
    
    > os.exit()
