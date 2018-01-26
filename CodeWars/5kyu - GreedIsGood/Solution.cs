using System;
using System.Linq;
using System.Collections.Generic;


public static class Kata
{
    private static int[] TripleScores = { -1, 1000, 200, 300, 400, 500, 600 };
    private static int[] IndividualScores = { -1, 100, 0, 0, 0, 50, 0 };
    
    private static Func<IGrouping<int,int>, int> ScoreDiceGroup = (group) =>
    {
        if (group.Count() >= 3)
            return TripleScores[group.Key] + ((group.Count() - 3) * IndividualScores[group.Key]);
            
        return group.Count() * IndividualScores[group.Key];
    };

    public static int Score(int[] dice) {
        return dice
            .GroupBy(x => x)
            .Sum(ScoreDiceGroup);
    }
}
