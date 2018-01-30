module RGBtoHEX

let adjustColorValue (x:int) : int =
    match x with
    | _ when x < 0 -> 0
    | _ when x > 255 -> 255
    | _ -> x

let rgb (r:int) (g:int) (b:int) : string =
    (
        (r |> adjustColorValue |> (*) 0x010000) +
        (g |> adjustColorValue |> (*) 0x000100) +
        (b |> adjustColorValue |> (*) 0x000001)
    )
    |> sprintf "%06x"
    |> (fun x -> x.ToUpper())
