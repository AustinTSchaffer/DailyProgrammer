namespace ShiftRegisters

[<AbstractClass>]
type LinearFeedbackShiftRegister (initialState:bigint, length) =
    inherit ShiftRegister (initialState, length)

    /// Defines a function that feeds the state of the shift
    /// register back into the input to the shift register
    abstract FeedbackFunction : unit -> bool

    /// The default feedback function.
    /// register back into the input to the shift register    
    default __.FeedbackFunction () = false

    new(initialState:int, length) = 
        LinearFeedbackShiftRegister(bigint initialState, length)

    new() = LinearFeedbackShiftRegister(0, 32)

    override this.Shift () = this.FeedbackFunction() |> this.Shift
