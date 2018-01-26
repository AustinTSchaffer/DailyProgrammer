module TenMinuteWalk

let walkLengthMinutes = 10

let isValidLength (walk:'a list) : bool =
    walk.Length = walkLengthMinutes

let toCardinalVector cardinalDir =
    match cardinalDir with
    | 'n' -> ( 0, 1)
    | 's' -> ( 0,-1)
    | 'e' -> ( 1, 0)
    | 'w' -> (-1, 0)
    | _   -> ( 0, 0)

let addVectors v1 v2 = (fst v1 + fst v2, snd v1 + snd v2)
    
let validEndingCoordinate (walk:char list) : bool = 
    walk
    |> List.map toCardinalVector
    |> List.reduce addVectors
    |> (=) (0,0)

let isValidWalk walk = 
    (validEndingCoordinate walk) && 
    (isValidLength walk)
