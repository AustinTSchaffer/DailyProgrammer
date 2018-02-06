/// Contains functions for determining if
/// any periods of time overlap, and how
/// much total time is covered. 
module PunchCardTotalTimeCalculator

open System

type PunchCard = {
    In : float;
    Out : float;
}

let overlapping (card1:PunchCard) (card2:PunchCard) = 
    (card1.In >= card2.In && card1.In <= card2.Out) ||
    (card2.In >= card1.In && card2.In <= card1.Out)

/// Combines 2 punch cards if their time ranges have any overlap
let merge (card1:PunchCard) (card2:PunchCard) = 
    if (card1, card2) ||> overlapping |> not  then
        failwith "PunchCards that do not overlap cannot be combined."
    { In = min card1.In card2.In; 
        Out = max card1.Out card2.Out }

let mergeAll punchcards = 
    let rec mergeLoop sortedPCs = 
        match sortedPCs with
        | [] | [_] -> sortedPCs 
        | [ x1; x2 ] when overlapping x1 x2 -> [ merge x1 x2 ]
        | [ _; _ ] -> sortedPCs
        | x1 :: x2 :: xs when overlapping x1 x2 -> mergeLoop (merge x1 x2 :: xs)
        | x1 :: xs -> x1 :: mergeLoop xs
    
    punchcards
    |> List.sortBy (fun pc -> pc.In)
    |> mergeLoop
    
let totalHours =
    mergeAll >>
    List.fold (fun total card -> total + (card.Out - card.In)) 0.0

/// Converts a string list, formatted `[ "in out"; ... ]`
/// where "in" and "out" are integers or floats, into a 
/// PunchCard list 
let convertToPunchCardsList = 
    List.map (
        (fun (str:string) -> str.Split [|' '|]) >>
        (Array.map Double.Parse) >> 
        (fun arr -> { In = arr.[0]; Out = arr.[1] })
    )
