type Instruction(direction: string, distance: int) =
    member this.Direction = direction
    member this.Distance = distance


let valueIsStairs = (=) 1
let tryFindStairsLoc = List.tryFindIndex valueIsStairs
let valueIsPerson = (=) 2
let tryFindPersonLoc = List.tryFindIndex valueIsPerson


let getOffLevelInstructions (carparkLevel: int list) (personLocationInLevel: int option) : Instruction list =
    let takeStairs stairsLoc personLoc =
        let distToStairs = personLoc - stairsLoc
        match sign distToStairs with
        | -1 -> [ Instruction("R", abs distToStairs); Instruction("D", 1) ]
        | +1 -> [ Instruction("L", abs distToStairs); Instruction("D", 1) ]
        | _ -> [ Instruction("D", 1) ]

    let goToExit personLoc =
        let distToExit = (List.length carparkLevel) - personLoc - 1
        match distToExit with
        | 0 -> []
        | _ -> [ Instruction("R", distToExit) ]

    match personLocationInLevel with
    | None -> []
    | Some personLoc ->
        match tryFindStairsLoc carparkLevel with
        | Some stairsLoc -> takeStairs stairsLoc personLoc
        | None -> goToExit personLoc


type CondenseInstructionsState(insts: Instruction list, consecutiveDowns: int) =
    member this.Instructions = insts
    member this.ConsecutiveDowns = consecutiveDowns


let condenseDownInstructions instructions =
    let initialState = CondenseInstructionsState([], 0)

    let manageState (state: CondenseInstructionsState) (instruction: Instruction) =
        let cdowns = state.ConsecutiveDowns
        let isDown = instruction.Direction = "D"

        if isDown then
            CondenseInstructionsState(state.Instructions, cdowns+1)
        else if cdowns = 0 then
            CondenseInstructionsState(List.append state.Instructions [instruction], 0)
        else
            CondenseInstructionsState(List.append state.Instructions [Instruction("D", cdowns); instruction], 0)

    let result = (List.fold manageState initialState instructions)

    if result.ConsecutiveDowns = 0 then
        result.Instructions
    else
        List.append result.Instructions [Instruction("D", result.ConsecutiveDowns)]


let formatInstruction (instruction: Instruction) = 
    sprintf "%s%i" instruction.Direction instruction.Distance


let solve (carpark: int list list) : string list =
    let initialState = (None, [])
    let manageState (state: int option * Instruction list) (carParkLevel: int list) =
        let prevInstructions = snd state
        let personOnLevel = tryFindPersonLoc carParkLevel

        let currentPersonLocation = 
            match personOnLevel with
            | Some personLoc -> Some personLoc
            | None -> fst state
        
        let nextPersonLocation =
            match fst state, personOnLevel with
            | None, None -> None
            | _, _ -> tryFindStairsLoc carParkLevel

        (
            nextPersonLocation, 
            List.append prevInstructions (getOffLevelInstructions carParkLevel currentPersonLocation)
        )
 
    (List.fold manageState initialState carpark) 
    |> snd
    |> condenseDownInstructions
    |> List.map formatInstruction
