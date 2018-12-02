# Ranking Poker Hands

A famous casino is suddenly faced with a sharp decline of their revenues. They
decide to offer Texas hold'em also online. Can you help them by writing an
algorithm that can rank poker hands?


## Task

Create a poker hand that has a method to compare itself to another poker hand:

```fs
PokerHand.compareWith: hand: PokerHand -> Result
```

A poker hand has a constructor that accepts a string containing 5 cards:

```fs
let hand = PokerHand("KS 2H 5C JD TD")
```

The characteristics of the string of cards are:
- A space is used as card seperator
- Each card consists of two characters
- The first character is the value of the card, valid characters are: 2, 3, 4,
  5, 6, 7, 8, 9, T(en), J(ack), Q(ueen), K(ing), 
- A(ce) The second character represents the suit, valid characters are:
  S(pades), H(earts), D(iamonds), C(lubs)

The result of your poker hand compare can be one of these 3 options:

```fs
type Result =
| Win = 0 
| Loss = 1
| Tie = 2
```

Apply the Texas Hold'em rules for ranking the cards. There is no ranking for the
suits.


## Solution

The solution seems to work locally, but does not seems to work when running it
on CodeWars.com, which was disappointing. The solution is pretty Enum-heavy,
mostly to combat the weird rules with Ace.

Some of the code turned into spaghetti, but it started off with good intentions.
After a few hours of tinkering, it turned into a slog, and then into "just get
it working".
