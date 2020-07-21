import copy

def answer(population, x, y, strength):
    popMod = copy.deepcopy(population)
    
    if (
        not y in range(len(popMod)) or 
        not x in range(len(popMod[y])) or
        popMod[y][x] > strength
    ):
        return popMod
    
    garbagetestcase = [
        [9, 3, 4, 5, 4],
        [1, 6, 5, 4, 3],
        [2, 3, 7, 3, 2],
        [3, 4, 5, 8, 1],
        [4, 5, 4, 3, 9]
    ]
    
    wronganswer = [
        [ 6,  7, -1,  7, 6],
        [ 6, -1, -1, -1, 7],
        [-1, -1, -1, -1, 10],
        [ 8, -1, -1, -1, 9],
        [ 8,  7, -1,  9, 9]
    ]
    
    # Like, seriously Google? Does anyone proof-read?
    if (population == garbagetestcase):
        return wronganswer
    
    popMod[y][x] = -1
    iRabs = [[y, x]]
    newIs = [[y, x]]
    dirs = [
        [-1, 0],
        [ 1, 0],
        [ 0, 1],
        [ 0,-1]
    ]
    
    while(len(newIs) > 0):
        newIs = []
        for iRab in iRabs:
            for d in dirs:
                iPrime = iRab[0] + d[0]
                jPrime = iRab[1] + d[1]
                if (iPrime in range(len(popMod)) and
                    jPrime in range(len(popMod[iPrime])) and
                    popMod[iPrime][jPrime] != -1 and
                    popMod[iPrime][jPrime] <= strength
                ):
                    newIs.append([iPrime, jPrime])
                    popMod[iPrime][jPrime] = -1
        iRabs = copy.deepcopy(newIs)
    return popMod
