module SFInterpreter

type BranchMapRecord = {
    left: int;
    right: int
}

type SFState = {
    program: string;
    branchMap: BranchMapRecord list;
    pcounter: int;
    tape: string;
    tapePtr: int
}


let currentValue state = 
    state.tape.[state.tapePtr]


type private BBMState = {
    stack: int list;
    map: BranchMapRecord list;
}


let buildBranchMap (code: string) : BranchMapRecord list =
    // for i,instruction in codeWithIndex:
    //     if instruction is lbracket:
    //         push i into stack
    //     if instruction is rbracket
    //         pop i2 from stack
    //         push (i2, i) into map

    (Seq.fold
        (fun state (i, ch) ->
            match ch with
            | '[' -> {state with stack = i::state.stack}
            | ']' -> {map = {right = i; left = (List.head state.stack)}::state.map; stack = List.tail state.stack}
            | _ -> state
        )
        {map=[]; stack=[]}
        (Seq.indexed code)
    ).map

let strReplaceIndex (str: string) (index: int) (newChar: char) =
    sprintf "%s%c%s"
        (str.Substring (0, index))
        newChar
        (str.Substring(index + 1))

let flipBit (state: SFState) =
    let newBit =
        if currentValue state = '0' then '1'
        else '0'

    {state with tape = (strReplaceIndex state.tape state.tapePtr newBit)}

let safeMoveLeft state =
    {
        state with
            tapePtr =
                if state.tapePtr <= 0 then 0
                else state.tapePtr - 1
    }

let safeMoveRight state =
    {
        state with 
            tapePtr = 
                if state.tapePtr >= state.tape.Length - 1 then 
                    state.tape.Length - 1
                else
                    state.tapePtr + 1
    }

let jumpBackIfNotZero (state: SFState) =
    if (currentValue state) = '1' then
        let branchMapRecord =
            List.find
                (fun s -> (s.right = state.pcounter))
                state.branchMap
        {state with pcounter = branchMapRecord.left}
    else
        state

let jumpForwardIfZero (state: SFState) =
    if (currentValue state) = '0' then
        let branchMapRecord =
            List.find
                (fun s -> (s.left = state.pcounter))
                state.branchMap
        {state with pcounter = branchMapRecord.right}
    else
        state

let executeCurrentInstruction (state: SFState) =
    match state.program.[state.pcounter] with
    | '*' -> flipBit state
    | '>' -> {state with tapePtr = state.tapePtr + 1}
    | '<' -> {state with tapePtr = state.tapePtr - 1}
    // | '>' -> safeMoveRight state
    // | '<' -> safeMoveLeft state
    | '[' -> jumpForwardIfZero state
    | ']' -> jumpBackIfNotZero state
    | _ -> state


let incrementProgramCounter (state: SFState) =
    {state with pcounter = state.pcounter + 1}


let exitCondition (state: SFState): bool =
    state.pcounter >= state.program.Length ||
    state.tapePtr >= state.tape.Length ||
    state.tapePtr < 0


let rec sfInterpreter (state: SFState) : SFState =
    if exitCondition state then
        state
    else
        state
        |> executeCurrentInstruction
        |> incrementProgramCounter
        |> sfInterpreter


let interpreter (code: string) (tape: string): string = 
    let initialState = {
        SFState.program = code;
        SFState.branchMap = buildBranchMap code;

        SFState.pcounter = 0;
        SFState.tape = tape
        SFState.tapePtr = 0;
    }
    
    (sfInterpreter initialState).tape
