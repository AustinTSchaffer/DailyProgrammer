module SFInterpreter.Interpreter


type SFState = {
    program: string;
    branchMap: BranchMap.BranchMapRecord list;
    pcounter: int;
    tape: string;
    tapePtr: int
}


let private currentValue state = 
    state.tape.[state.tapePtr]


let private replaceIndex (str: string) (index: int) (newChar: char) =
    sprintf "%s%c%s"
        (str.Substring (0, index))
        newChar
        (str.Substring(index + 1))


let private flipBit (state: SFState) =
    let newBit =
        if currentValue state = '0' then '1'
        else '0'

    {state with tape = (replaceIndex state.tape state.tapePtr newBit)}


let private safeMoveLeft state =
    {
        state with
            tapePtr =
                if state.tapePtr <= 0 then 0
                else state.tapePtr - 1
    }

let private safeMoveRight state =
    {
        state with 
            tapePtr = 
                if state.tapePtr >= state.tape.Length - 1 then 
                    state.tape.Length - 1
                else
                    state.tapePtr + 1
    }

let private jumpBackIfNotZero (state: SFState) =
    if (currentValue state) = '1' then
        let branchMapRecord =
            List.find
                (fun (s: BranchMap.BranchMapRecord) -> (s.right = state.pcounter))
                state.branchMap
        {state with pcounter = branchMapRecord.left}
    else
        state

let private jumpForwardIfZero (state: SFState) =
    if (currentValue state) = '0' then
        let branchMapRecord =
            List.find
                (fun (s: BranchMap.BranchMapRecord) -> (s.left = state.pcounter))
                state.branchMap
        {state with pcounter = branchMapRecord.right}
    else
        state


let internal exitCondition (state: SFState): bool =
    state.pcounter >= state.program.Length ||
    state.tapePtr >= state.tape.Length ||
    state.tapePtr < 0


let internal executeCurrentInstruction (state: SFState) =
    match state.program.[state.pcounter] with
    | '*' -> flipBit state
    | '>' -> {state with tapePtr = state.tapePtr + 1}
    | '<' -> {state with tapePtr = state.tapePtr - 1}
    // | '>' -> safeMoveRight state
    // | '<' -> safeMoveLeft state
    | '[' -> jumpForwardIfZero state
    | ']' -> jumpBackIfNotZero state
    | _ -> state


let internal incrementProgramCounter (state: SFState) =
    {state with pcounter = state.pcounter + 1}
