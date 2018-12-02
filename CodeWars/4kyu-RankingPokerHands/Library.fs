module PokerHand

type Value = 
    | Two = 2
    | Three = 3
    | Four = 4
    | Five = 5
    | Six = 6
    | Seven = 7
    | Eight = 8
    | Nine = 9
    | Ten = 10
    | Jack = 11
    | Queen = 12
    | King = 13
    | Ace = 14

type Suit =
    | Spades = 'S'
    | Hearts = 'H'
    | Clubs = 'C'
    | Diamonds = 'D'

type PokerHandRank =
    | HighCard = 0
    | Pair = 1
    | TwoPairs = 2
    | ThreeOfAKind = 3
    | Straight = 4
    | Flush = 5
    | FullHouse = 6
    | FourOfAKind = 7
    | StraightFlush = 8

type Result =
    | Win = 0 
    | Loss = 1
    | Tie = 2
    
let valueCharToValue (card: char): Value =
    match card with
    | 'A' -> Value.Ace
    | 'T' -> Value.Ten
    | 'J' -> Value.Jack
    | 'Q' -> Value.Queen
    | 'K' -> Value.King
    | _ -> 
    (
        card
        |> System.Char.GetNumericValue
        |> int
        |> LanguagePrimitives.EnumOfValue<int, Value>
    )


let suitCharToSuit = 
    LanguagePrimitives.EnumOfValue<char, Suit>


type Card (value: Value, suit: Suit) =
    member this.Value = value
    member this.Suit = suit
    static member ParseCardString (cardstring: string) =
        Card(valueCharToValue cardstring.[0], suitCharToSuit cardstring.[1])


let isFlush (hand: Card[]) = 
    hand 
    |> Array.map (fun (c: Card) -> c.Suit)
    |> Array.distinct
    |> Array.length
    |> (=) 1


let isStraight (hand: Card[]) =
    let sortedNonAces = 
        hand
        |> Array.map (fun (card: Card) -> card.Value)
        |> Array.filter (fun value -> value <> Value.Ace)
        |> Array.sort

    if sortedNonAces.Length < 4 then 
        false
    else
        let nonAcesAreStraight =
            sortedNonAces
            |> Array.pairwise
            |> Array.forall (fun (v1, v2) -> (int v1 + 1) = int v2)

        nonAcesAreStraight && (
            sortedNonAces.Length = 5 ||
            Value.Two = sortedNonAces.[0] ||
            Value.King = Array.last sortedNonAces
        )

type CardGrouping = {
    value: Value;
    quantity: int;
}

let cardGroupings (hand: Card[]) = 
    hand 
    |> Seq.groupBy (fun card -> card.Value)
    |> Seq.map (fun g -> 
        {
            CardGrouping.value = fst g;
            CardGrouping.quantity = Seq.length (snd g)
        })
    |> Seq.filter (fun cg -> cg.quantity > 1)
    |> Seq.toList


let cardOrderForStraights (hand: Card[]) =
    // Sort by its integer value
    let sortedCardValues = 
        hand
        |> Array.map (fun card -> card.Value)
        |> Array.sort

    let isBabyStraight =
        (sortedCardValues |> Array.contains Value.Ace) &&
        (sortedCardValues |> Array.contains Value.Five)

    let highCard = 
        if isBabyStraight then Value.Five
        else Array.last sortedCardValues
            
    List.singleton highCard


let cardOrderForCardGroupings (hand: Card[]) (cardGroupings: CardGrouping list) =
    let valuesOrderedByGroupSizeThenValue = 
        cardGroupings
        |> List.sortBy (fun cg -> cg.quantity, cg.value)
        |> List.map (fun cg -> cg.value)

    let kickers = 
        hand
        |> List.ofArray
        |> List.map (fun c -> c.Value)                    
        |> List.filter (fun value -> 
            not (
                cardGroupings 
                |> List.map (fun cg -> cg.value)
                |> List.contains value
            ))

    List.append valuesOrderedByGroupSizeThenValue kickers

let getGroupOfSize (groupSize: int) (cardGroupings: CardGrouping list) =
    cardGroupings
    |> List.find (fun cg -> cg.quantity = groupSize)

let containsGroupOfSize (groupSize: int) (cardGroupings: CardGrouping list) =
    cardGroupings
    |> List.map (fun cg -> cg.quantity)
    |> List.contains groupSize



type PokerHandInfo (rank: PokerHandRank, cardOrder: Value list) =

    member this.Rank = rank
    member this.CardOrder = cardOrder

    static member GetInfo (hand: Card[]) : PokerHandInfo = 
        let handIsStraight = isStraight hand
        let cardGroupings = cardGroupings hand
        let handIsFlush = isFlush hand

        let cardOrder = 
            if handIsStraight then
                cardOrderForStraights hand
            else if not (List.isEmpty cardGroupings) then
                cardOrderForCardGroupings hand cardGroupings
            else
                hand
                |> List.ofArray
                |> List.map (fun card -> card.Value)
                |> List.sort

        let handRank = 
            fun (phr: PokerHandRank) -> 
                PokerHandInfo(phr, cardOrder)

        if handIsStraight && handIsFlush then
            handRank PokerHandRank.StraightFlush

        else if handIsStraight then
            handRank PokerHandRank.Straight

        else if handIsFlush then
            handRank PokerHandRank.Flush

        else if cardGroupings |> containsGroupOfSize 4 then
            handRank PokerHandRank.FourOfAKind

        // 3ofakind and fullhouse 
        else if cardGroupings |> containsGroupOfSize 3 then
            if cardGroupings |> containsGroupOfSize 2 then 
                handRank PokerHandRank.FullHouse
            else
                handRank PokerHandRank.ThreeOfAKind

        // Pairs
        else if cardGroupings |> containsGroupOfSize 2 then
            let firstPair = 
                cardGroupings 
                |> getGroupOfSize 2

            let withoutFirstPair = 
                cardGroupings
                |> List.filter (fun cg -> cg.value <> firstPair.value)

            if withoutFirstPair |> containsGroupOfSize 2 then
                handRank PokerHandRank.TwoPairs
            else 
                handRank PokerHandRank.Pair

        else
            handRank PokerHandRank.HighCard


    member this.CompareWith (other: PokerHandInfo): Result =
        let winLossElse me opponent tie =
            if me > opponent then Result.Win
            else if me < opponent then Result.Loss
            else tie()

        // Compare Ranks. If ranks are the same, compare card orders.
        // Card orders are lists of card values, presumably the same 
        // length each. If those are the same, then true tie detected.
        winLossElse this.Rank other.Rank (fun () ->
            (
                List.map2
                    (fun me opponent -> winLossElse me opponent (fun () -> Result.Tie))
                    this.CardOrder
                    other.CardOrder
            )
            |> List.tryFind (fun result -> result <> Result.Tie) 
            |> function
                | Some result -> result
                | None -> Result.Tie
        )



type Pokerhand (hand: string) =
    member this.Hand = hand.Split(' ') |> Array.map Card.ParseCardString

    member this.compareWith (pokerhand: Pokerhand) =
        (PokerHandInfo.GetInfo this.Hand).CompareWith(PokerHandInfo.GetInfo pokerhand.Hand)
        