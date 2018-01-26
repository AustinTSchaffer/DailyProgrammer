module DontGiveMeFive

let rec numberContains k n =
    match n with
    | n when (abs (n%10)) = (abs k) -> true
    | 0 -> false
    | _ -> (n/10) |> numberContains k 

let numbersWithout k startValue endValue =
    [ startValue .. endValue ]
    |> List.filter (numberContains k >> not)

let dontGiveMeFive startValue endValue =
    numbersWithout 5 startValue endValue
    |> List.length
