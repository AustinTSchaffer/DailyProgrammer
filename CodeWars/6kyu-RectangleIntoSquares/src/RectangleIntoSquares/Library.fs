module RectangleIntoSquares

let squaresInRect length width =
    let rec _squaresInRect _length _width =
        if _length = _width then
            [ _length ]
        else
            let mini = min _length _width
            let maxi = max _length _width
            mini :: _squaresInRect (maxi - mini) mini
        
    if length = width then None
    else Some (_squaresInRect length width)
