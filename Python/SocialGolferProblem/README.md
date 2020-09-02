# Social Golpher Problem

The social golpher problem is a rather famous computer science and math problem
involving grouping objects together, such that no 2 objects have not previously
been matched in the same group. Someone [posed this problem on the /r/python subreddit](https://www.reddit.com/r/Python/comments/cvluxp/44_players_split_into_groups_of_4_for_3_games/).
As it turns out, the solution for 11 groups of players is rather trivial.

The original problem called for a solution to

- play 3 rounds of golf
- with 11 groups of golfers
- with 4 golfers in each group
- such that no golfers play any other golfer more than once.

This solution shows that it is possible to

- play up to 11 rounds of golf
- with 11 groups of golfers
- with up to 11 golfers in each group
- such that no golfers play any other golfer more than once.

## Solution

Someone on the same thread rephrased the problem in terms of stacked hula-hoops.

You can represent the number of players in each group as the number of hula-hoops
that are stacked. You can then represent each group as a shared label that is
written across each hula-hoop. In this case, there should be 11 distinct labels,
each written in the same order on each hula-hoop, each written 1/11th of the way
around each hoop. You can represent the first round by repositioning each hoop, such that
all of the shared labels line up between each hoop. You can then represent subsequent
rounds by repositioning each hoop, such that no labels line up between any of the hoops.
The algorithm for repositioning each hoop in the case of 11 groups, is to rotate each
hoop by a fixed amount each time.

- The bottom hoop never moves.
- The 1st hoop is rotated 1/11th of a rotation each round.
- The Nth hoop is rotated N/11ths of a rotation each round.

The python script in `sgp.py` models this rephrasing of the problem, except it uses
the terms `groups` and `objects` wherever appropriate, to genericize the problem
as much as possible.

Given that 11 is prime, I suspect that using this script for any prime number of groups will result
in a value that is equal to the number of groups, as long as the number of objects per group is less than
or equal to the number of groups. As long as those input conditions are met, this terrible
script should work.
