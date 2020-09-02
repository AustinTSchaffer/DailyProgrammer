# Higher-or-Lower

The objective of the game higher-or-lower is to iteratively guess whether the
next card drawn from a standard deck of cards will be higher or lower than the
card previously drawn from that deck of cards. The objective of this Python
project is to determine how likely a rational player will win.

In the version of the game that this project was designed to simulate: 

- 4 cards will be drawn from the deck in total.
- If you guess correctly 3 times, you win. 
- If you guess any wrong, you lose.
- Ace is high.

## Results

There are 6,497,400 possible permutations of 4 cards from a standard deck of 52
playing cards. This equals the number of distinct games that can be played
assuming the rules above.

    (52 nCr 4) = 270,725
    (4 nPr 4) = 24
    (52 nPr 4) = (52 nCr 4) * (4 nPr 4) = 6,497,400

If a strictly rational agent plays all 6.5 million games, it will win 2,274,240
of those games and lose 4,223,160 of them. This is a win percentage of
approximately 35%.

If you are placing bets on winning this version of the game, you will need to
make sure that the payout is at least 2.86 times the starting bet in order to
make profit. If the payout is lower than that, the house wins.
