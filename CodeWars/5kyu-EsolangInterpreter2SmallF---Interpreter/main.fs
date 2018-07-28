module SFInterpreter.Main

open Interpreter

let interpreter (code: string) (tape: string): string = 
    let initialState = {
        SFState.program = code;
        SFState.branchMap = BranchMap.buildBranchMap code;

        SFState.pcounter = 0;
        SFState.tape = tape;
        SFState.tapePtr = 0;
    }

    let rec interpreter (state: SFState) : SFState =
        if exitCondition state then
            state
        else
            state
            |> executeCurrentInstruction
            |> incrementProgramCounter
            |> interpreter
    
    (interpreter initialState).tape
