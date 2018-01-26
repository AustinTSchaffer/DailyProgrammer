module PiApproximation

open System


/// Computes the difference between x and y
let diff x y = x - y |> abs


/// Computes the Nth fraction in the Leibniz Pi generation sequence, 
/// 0 based indexes.
let leibnizSequence index =
    let n = if ((index) % 2 = 0) then 1.0 else -1.0
    let d = ((2.0 * (float index)) + 1.0)
    n/d


/// Computes a sequence of tuples that are equivalent to
/// (1) the number of iterations of the Leibniz Pi formula
/// to reach (2) an approximation of PI/4.
let leibnizPiAccumulation : seq<int*float> =
    (0, 0.0) |> Seq.unfold (fun state -> 
        let n,approxPi4 = state
        Some ((n, approxPi4), (n+1, approxPi4 + (leibnizSequence n)))
    )

    
/// Computes the number of iterations of Leibniz's formula for 
/// Pi it takes in order to calculate Pi to within the given 
/// epsilon.
let iterPi (epsilon:float) : (int*float) =
    leibnizPiAccumulation 
    |> Seq.map (fun piTuple -> (fst piTuple, snd piTuple * 4.0))
    |> Seq.find (snd >> (diff Math.PI) >> (fun diff -> diff < epsilon))
