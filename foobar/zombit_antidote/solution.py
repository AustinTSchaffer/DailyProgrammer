import itertools

def answer(meetings):
    curMax = 0
    for i in range(0, len(meetings)+1):
        for comb in itertools.combinations(meetings, i):
            if not hasoverlap(comb) and len(comb) > curMax:
                curMax = len(comb)
    return curMax


def hasoverlap(meetings):
    for mA in meetings:
        for mB in meetings:
            if mA is not mB and (
                (mB[0] >= mA[0] and mB[0] <  mA[1]) or
                (mB[1] >  mA[0] and mB[1] <= mA[1])
            ):
                return True
    return False
