module Tests

open System
open BalancingMySpending
open Xunit
open Xunit.Sdk

let assertEqualIntLists (expected:int list) (actual:int list) = 
    printf "Expected: %A\n" expected
    printf "Actual:   %A\n" actual
    Assert.Equal<Collections.Generic.IEnumerable<int>>(expected, actual);

[<Fact>]
let ``Test Empty`` () =
    assertEqualIntLists [] (balance [])
    assertEqualIntLists [] (balance [])

[<Fact>]
let ``Test Zero`` () =
    assertEqualIntLists [0] (balance [0])
    assertEqualIntLists [0] (balance [0.0])

[<Fact>]
let ``n zeros yields [0 .. n-1]`` () =
    let input1 = Seq.toList <| Seq.init 100 (fun _ -> 0)
    let input2 = Seq.toList <| Seq.init 100 (fun _ -> 0.0)
    let expected = [0 .. 99]

    assertEqualIntLists expected (balance input1)
    assertEqualIntLists expected (balance input2)

[<Fact>]
let ``TesCase 1`` () = 
    let expected = [ 0; 3; 7 ]
    assertEqualIntLists expected (balance [0; -3; 5; -4; -2; 3; 1; 0])
    assertEqualIntLists expected (balance [0.0; -3.0; 5.0; -4.0; -2.0; 3.0; 1.0; 0.0])
    assertEqualIntLists expected (balance [0.0; -0.3; 0.5; -0.4; -0.2; 0.3; 0.1; 0.0]) // TODO: Why is this failing?

[<Fact>]
let ``Test Case 2`` () =
    let expected = [5]
    assertEqualIntLists expected (balance [ 3; -2; 2; 0; 3; 4; -6; 3; 5; -4; 8 ])

[<Fact>]
let ``Test Case 3`` () =
    let expected = [8]
    assertEqualIntLists expected (balance [ 9; 0;-5; -4; 1; 4; -4; -9; 0; -7; -1 ])


[<Fact>]
let ``Test Case 4`` () =
    let expected = [6]
    assertEqualIntLists expected (balance [ 9; -7; 6; -8; 3; -9; -5; 3; -6; -8; 5 ])
    assertEqualIntLists expected (balance [ 9.0; -7.0; 6.0; -8.0; 3.0; -9.0; -5.0; 3.0; -6.0; -8.0; 5.0 ])
    assertEqualIntLists expected (balance [ 0.9; -0.7; 0.6; -0.8; 0.3; -0.9; -0.5; 0.3; -0.6; -0.8; 0.5 ])
