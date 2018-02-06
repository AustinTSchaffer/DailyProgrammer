module Tests

open Xunit
open PunchCardTotalTimeCalculator
open System

[<Fact>]
let ``Test general overlapping, forwards and backwards`` () =
    let p1 = { In = 0.0; Out = 3.0 }
    let p2 = { In = 2.0; Out = 4.0 }
    let p3 = { In = 3.5; Out = 6.0 }
    let p4 = { In = 5.9; Out = 6.1 }
    let p5 = { In = 6.0; Out = 10.0 }

    Assert.True (overlapping p1 p2)
    Assert.False (overlapping p1 p3)
    Assert.False (overlapping p1 p4)
    Assert.False (overlapping p1 p5)

    Assert.True (overlapping p2 p1)
    Assert.True (overlapping p2 p3)
    Assert.False (overlapping p2 p4)
    Assert.False (overlapping p2 p5)

    Assert.False (overlapping p3 p1)
    Assert.True (overlapping p3 p2)
    Assert.True (overlapping p3 p4)
    Assert.True (overlapping p3 p5)

    Assert.False (overlapping p4 p1)
    Assert.False (overlapping p4 p2)
    Assert.True  (overlapping p4 p3)
    Assert.True  (overlapping p4 p5)

    Assert.False (overlapping p5 p1)
    Assert.False (overlapping p5 p2)
    Assert.True (overlapping p5 p3)
    Assert.True (overlapping p5 p4)

[<Fact>]
let ``Time periods overlap themselves`` () =
    [
        { In = 0.0; Out = 3.0 }; { In = 2.0; Out = 4.0 };
        { In = 3.5; Out = 6.0 }; { In = 5.9; Out = 6.1 };
        { In = 6.0; Out = 10.0 } 
    ]
    |> List.forall (fun p -> overlapping p p)
    |> Assert.True

let lengthTestCase expected = 
    convertToPunchCardsList 
    >> totalHours 
    >> (=) expected 
    >> Assert.True 

[<Fact>]
let ``Length test case 1`` () = 
    [ "1 3"; "2 3"; "4 5" ]
    |> lengthTestCase 3.0 

[<Fact>]
let ``Length test case 2`` () =
    [ "2 4"; "3 6"; "1 3"; "6 8" ]
    |> lengthTestCase 7.0

[<Fact>]
let ``Length test case 3`` () =
    [ "2 4"; "3 6"; "1 3"; "6 8" ]
    |> lengthTestCase 7.0

[<Fact>]
let ``Length test case 4`` () =
    [ "6 8"; "5 8"; "8 9"; "5 7"; "4 7" ]
    |> lengthTestCase 5.0

[<Fact>]
let ``Length test case 5`` () =
    [ 
        "15 18"; "13 16"; "9 12"; "3 4";
        "17 20"; "9 11"; "17 18"; "4 5";
        "5 6"; "4 5"; "5 6"; "13 16";
        "2 3"; "15 17"; "13 14";
    ]
    |> lengthTestCase 14.0
