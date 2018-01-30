module Tests

open Xunit
open RGBtoHEX

[<Fact>]
let ``All integers are 0`` () =
    Assert.Equal("000000", rgb 0 0 0)

[<Fact>]
let ``All integers are 255`` () =
    Assert.Equal("FFFFFF", rgb 255 255 255)

[<Fact>]
let ``Any integer greater than 255`` () =
    Assert.Equal("FF0000", rgb 999  0   0 )
    Assert.Equal("00FF00", rgb  0  999  0 )
    Assert.Equal("0000FF", rgb  0   0  999)
    Assert.Equal("00FFFF", rgb  0  999 999)
    Assert.Equal("FF00FF", rgb 999  0  999)
    Assert.Equal("FFFF00", rgb 999 999  0 )
    Assert.Equal("FFFFFF", rgb 999 999 999)

[<Fact>]
let ``Any integer less than 0`` () =
    Assert.Equal("00FFFF", rgb  -1 255 255)
    Assert.Equal("FF00FF", rgb 255 -1  255)
    Assert.Equal("FFFF00", rgb 255 255  -1)
    Assert.Equal("0000FF", rgb  -1  -1 255)
    Assert.Equal("00FF00", rgb  -1 255  -1)
    Assert.Equal("FF0000", rgb 255  -1  -1)
    Assert.Equal("000000", rgb  -1  -1  -1)

[<Fact>]
let ``Value out of bounds combination`` () =
    Assert.Equal("000000", rgb  -1  -1  -1)
    Assert.Equal("00FFFF", rgb  -1 999 999)
    Assert.Equal("0000FF", rgb  -1  -1 999)
    Assert.Equal("FF00FF", rgb 999  -1 999)
    Assert.Equal("FF0000", rgb 999  -1  -1)
    Assert.Equal("FFFF00", rgb 999 999  -1)
    Assert.Equal("00FF00", rgb  -1 999  -1)
    Assert.Equal("FFFFFF", rgb 999 999 999)

[<Fact>]
let ``All characters uppercase`` () =
    Assert.Equal("ABCDEF", rgb 171 205 239)
    
[<Fact>]
let ``Other assorted tests`` () =    
    Assert.Equal("9400D3", rgb 148 0 211)
    Assert.Equal("9400D3", rgb 148 -20 211)
    Assert.Equal("90C3D4", rgb 144 195 212)
    Assert.Equal("D4350C", rgb 212 53 12)
