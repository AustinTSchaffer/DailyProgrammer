# Million Bank Balance Puzzle (MPMP Puzzle 6)

_Alternate Title: Overly Generous Bank Interest Program_

> A bank is running a competition. You can make two deposits (of integer pounds)
> on two consecutive days and everyday the bank will add your last two balances
> together to give you a new balance.

> For example: You deposit £10 on day 1 and £20 on day 2. Your balance on day 1
> would be £10, day 2 £30, day 3 £40, day 4 £70 and so on.....

> You can keep the money if your balance eventually equals one million pounds
> exactly. If more than one person hits a million exactly, the prize goes to the
> person who took the longest to get there.

> Challenge: What must your initial two deposits be to ensure that you
> win the million pounds?


## Submission

If you deposit $144 on one day and $154 on the next (or vice versa), given the
bank's deal, it will take 19 days for the balance to reach 1,000,000.

| Day | Balance ($) |
| --- | ----------- |
| 1   | 144         |
| 2   | 298         |
| 3   | 442         |
| 4   | 740         |
| 5   | 1182        |
| 6   | 1922        |
| 7   | 3104        |
| 8   | 5026        |
| 9   | 8130        |
| 10  | 13156       |
| 11  | 21286       |
| 12  | 34442       |
| 13  | 55728       |
| 14  | 90170       |
| 15  | 145898      |
| 16  | 236068      |
| 17  | 381966      |
| 18  | 618034      |
| 19  | 1000000     |

`output.csv` contains a bunch of other results as well. The next-longest
possible submission that I came across is ($130, $1429), which takes 16 days to
reach $1,000,000.


## Possible Future Improvements

For one, the challenge specifies that both of the 2 deposits must be integers,
but does not specify that both must be positive. There may be a longer route
that includes a negative number as one of the initial "deposits", also known as
a "withdrawal". I did not explore that as a possibility.

The results in `output.csv` are not ordered by the number of days it will take
to reach 1,000,000. Instead, it is ordered by "deposit 2", then by "deposit 1",
which matches the order of the output of the `generate_distinct_integer_pairs`
function. That function generates pairs by incrementing one number, then
outputting that number along with all of the numbers from 0 up to and including
that number, which is why the output is ordered that way. If I instead used a
function that generated integer pairs ordered by the sum of the 2 values, that
might make the output of the script ordered by the number of days.

I would also like to generate all possible results creating an exhaustive
`output.csv` instead of just "the first 176 results that were generated by the
script before I terminated the program". I don't believe that would take too
much time to complete, but I'm not sure that my laptop would survive the
journey.
