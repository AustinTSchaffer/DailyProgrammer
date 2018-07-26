module Tests

open Xunit
open System
open RectangleIntoSquares

[<Fact>]
let ``Identity Tests`` () =
    Assert.Equal(None, squaresInRect 5 5)
    Assert.Equal(None, squaresInRect 53 53)
    Assert.Equal(None, squaresInRect Int32.MaxValue Int32.MaxValue)

[<Fact>]
let ``Vertical Same as Horizontal`` () =
    Assert.Equal(Some [3; 2; 1; 1], squaresInRect 5 3)
    Assert.Equal(Some [3; 2; 1; 1], squaresInRect 3 5)
    Assert.Equal(squaresInRect 5 3, squaresInRect 3 5)

[<Fact>]
let ``Long Rectangles`` () =

    let longRectangleTest length =
        let expected = [for _ in 1 .. length -> 1]
        Assert.Equal(Some expected, squaresInRect length 1) 
        Assert.Equal(Some expected, squaresInRect 1 length) 

    longRectangleTest 10
    longRectangleTest 100
    longRectangleTest 1000
    // longRectangleTest 10000 // too slow

[<Fact>]
let ``Golden Ratio `` () =
    let expected = [ 1000; 618; 382; 236; 146; 90; 56; 34; 22; 12; 10; 2; 2; 2; 2; 2 ]
    Assert.Equal(Some expected, squaresInRect 1618 1000)
    Assert.Equal(Some expected, squaresInRect 1000 1618)
