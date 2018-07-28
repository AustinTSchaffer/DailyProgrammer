module SFInterpreter.BranchMap

/// Keeps track of the instruction pointers of a `[` and its 
/// corresponding `]`.
type BranchMapRecord = {
    left: int;
    right: int
}

/// Type used to hold the state for the branch map builder. Type is
/// internal to the BranchMap module.
type private BBMState = {
    stack: int list;
    map: BranchMapRecord list;
}

/// Modifies the state in the event a `]` is found, kicking off
/// the corresponding stack and list operations.
let private foundRightBracket (state) (rIndex) : BBMState =
    let newBMR = {
        right = rIndex;
        left=(List.head state.stack)
    }

    {state with
        BBMState.map = newBMR::state.map; 
        BBMState.stack = List.tail state.stack
    }

/// Builds a branch map from a properly formatted sf program. Every `[`
/// character is matched up with its corresponding `]` character, keeping
/// any nesting in mind. Outputs a list of `BranchMapRecord`s, each holding
/// the instruction pointers to the matched brackets.
let buildBranchMap (code: string) : BranchMapRecord list =
    
    // pseudocode:
    //
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
            | ']' -> foundRightBracket state i
            | _ -> state
        )
        {map=[]; stack=[]}
        (Seq.indexed code)
    ).map

