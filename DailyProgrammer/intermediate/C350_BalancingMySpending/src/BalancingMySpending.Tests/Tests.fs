module Tests

open System
open BalancingMySpending
open Xunit

let assertEqualIntLists (expected:int list) (actual:int list) = 
    Assert.Equal<Collections.Generic.IEnumerable<int>>(expected, actual);

let assertEqualFloatLists (expected:int list) (actual:int list) = 
    Assert.Equal<Collections.Generic.IEnumerable<int>>(expected, actual);

[<Fact>]
let ``Test Empty`` () =
    assertEqualIntLists [] (balance [])
    assertEqualFloatLists [] (balance [])

[<Fact>]
let ``Test Zero`` () =
    assertEqualIntLists [0] (balance [0])
    assertEqualFloatLists [0] (balance [0.0])

[<Fact>]
let ``Test Case 1`` () = 
    let expected = [0; 3; 7]
    assertEqualIntLists expected (balance [0; -3; 5; -4; -2; 3; 1; 0])
    assertEqualFloatLists expected (balance [0.0; -3.0; 5.0; -4.0; -2.0; 3.0; 1.0; 0.0])

[<Fact>]
let ``n zeros yields [0 .. n-1]`` () =
    let input = Seq.toList <| Seq.init 100 (fun _ -> 0)
    let expected = [0 .. 99]
    assertEqualIntLists expected (balance input)



