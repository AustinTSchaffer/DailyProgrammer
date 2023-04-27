namespace ShiftRegisters

open System

/// Defines a shift register with an initial state and a constant number of 
/// bits.
type ShiftRegister (initialState:bigint, length:int) =
    
    do 
        if (initialState >= pown (bigint 2) (length)) then 
            failwith (sprintf "The initial state must be representable by %d bits" length)

    let _newShiftValue = pown (bigint 2) (length - 1)
    let mutable _state = initialState


    //#region constructors


    /// Default constructor, initializes an empty 32-bit shift register.
    new() = ShiftRegister(bigint 0, 32)
    
    /// Contstructor that takes an integer instead of a big integer as the 
    /// initial state.
    new(initialState:int, length) = ShiftRegister(bigint initialState, length)


    //#endregion
    //#region members


    /// The number of bits in this shift register.
    member val Length = length

    /// The internal state of the shift register.
    member __.State with get () = _state

    /// Shifts the register one bit to the right.
    /// Returns the internal state after shifting.
    abstract member Shift : unit -> bigint

    /// Shifts the register one bit to the right.
    /// Returns the internal state after shifting.
    default this.Shift () =
        _state <-
            (_state >>> 1)
        this.State        

    /// Shifts the register one bit to the right.
    /// Allows the input of a bit into the leftmost register.
    /// Returns the internal state after shifting.
    abstract member Shift : bool -> bigint

    /// Shifts the register one bit to the right.
    /// Allows the input of a bit into the leftmost register.
    /// Returns the internal state after shifting.
    default this.Shift (input:bool) = 
        _state <- 
            (_state >>> 1) ||| 
            (if input then _newShiftValue else 0I)
        this.State

    /// Returns the i^th bit of the internal state. 
    ///   - Bit 0 is the LSB
    ///   - Bit (this.Length - 1) is the MSB
    /// Note: If index is greater than the shift register's
    /// length, then the bit is considered false.
    member this.GetBit index = 
        if index > this.Length then
            false
        else
            this.State.ToByteArray().[index / 8]
            |> (&&&) (1uy <<< (index % 8))
            |> (<>) 0uy


    override this.ToString () =
        sprintf "0x%s" (
            this.State.ToByteArray()
            |> Array.rev
            |> Array.map (sprintf "%02X")
            |> String.concat "")

    //#endregion
