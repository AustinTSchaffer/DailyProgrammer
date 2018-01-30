module Tests

open Xunit

[<Fact>]
let ``All integers are 0`` () =
    Assert.Equal("000000", RGBtoHEX.rgb 0 0 0)

[<Fact>]
let ``All integers are 255`` () =
    Assert.Equal("FFFFFF", RGBtoHEX.rgb 255 255 255)

[<Fact>]
let ``Any integer greater than 255`` () =
    Assert.Equal("FF0000", RGBtoHEX.rgb 999  0   0 )
    Assert.Equal("00FF00", RGBtoHEX.rgb  0  999  0 )
    Assert.Equal("0000FF", RGBtoHEX.rgb  0   0  999)
    Assert.Equal("00FFFF", RGBtoHEX.rgb  0  999 999)
    Assert.Equal("FF00FF", RGBtoHEX.rgb 999  0  999)
    Assert.Equal("FFFF00", RGBtoHEX.rgb 999 999  0 )
    Assert.Equal("FFFFFF", RGBtoHEX.rgb 999 999 999)

[<Fact>]
let ``Any integer less than 0`` () =
    Assert.Equal("00FFFF", RGBtoHEX.rgb  -1 255 255)
    Assert.Equal("FF00FF", RGBtoHEX.rgb 255 -1  255)
    Assert.Equal("FFFF00", RGBtoHEX.rgb 255 255  -1)
    Assert.Equal("0000FF", RGBtoHEX.rgb  -1  -1 255)
    Assert.Equal("00FF00", RGBtoHEX.rgb  -1 255  -1)
    Assert.Equal("FF0000", RGBtoHEX.rgb 255  -1  -1)
    Assert.Equal("000000", RGBtoHEX.rgb  -1  -1  -1)

[<Fact>]
let ``Value out of bounds combination`` () =
    Assert.Equal("000000", RGBtoHEX.rgb  -1  -1  -1)
    Assert.Equal("00FFFF", RGBtoHEX.rgb  -1 999 999)
    Assert.Equal("0000FF", RGBtoHEX.rgb  -1  -1 999)
    Assert.Equal("FF00FF", RGBtoHEX.rgb 999  -1 999)
    Assert.Equal("FF0000", RGBtoHEX.rgb 999  -1  -1)
    Assert.Equal("FFFF00", RGBtoHEX.rgb 999 999  -1)
    Assert.Equal("00FF00", RGBtoHEX.rgb  -1 999  -1)
    Assert.Equal("FFFFFF", RGBtoHEX.rgb 999 999 999)

[<Fact>]
let ``All characters uppercase`` () =
    Assert.Equal("ABCDEF", RGBtoHEX.rgb 171 205 239)
    
[<Fact>]
let ``Other assorted tests`` () =    
    Assert.Equal("9400D3", RGBtoHEX.rgb 148 0 211)
    Assert.Equal("9400D3", RGBtoHEX.rgb 148 -20 211)
    Assert.Equal("90C3D4", RGBtoHEX.rgb 144 195 212)
    Assert.Equal("D4350C", RGBtoHEX.rgb 212 53 12)
