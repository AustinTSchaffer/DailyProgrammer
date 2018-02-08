module BalancingMySpending

/// Returns an ordered list containing the indexes at
/// which the sum of the elements 0 through x is equal
/// to the sums of the sum of the elements x through the
/// end of the list.
let inline balance list =
    let rec _balance leftSum rightSum indexedList =
        match indexedList with
        | x::xs when (leftSum = rightSum - snd x) -> fst x :: _balance (leftSum + snd x) (rightSum - snd x) xs
        | x::xs -> _balance (leftSum + snd x) (rightSum - snd x) xs
        | [] -> []

    _balance LanguagePrimitives.GenericZero (List.sum list) (List.indexed list)
