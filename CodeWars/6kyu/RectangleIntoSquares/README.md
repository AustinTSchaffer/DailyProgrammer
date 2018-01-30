# Rectangle Into Squares (6 kyu)

The drawing below gives an idea of how to cut a given "true" rectangle into 
squares ("true" rectangle meaning that the two dimensions are different). 

![](../../images/squaredrectangle.jpg)

You will be given two dimensions

    a positive integer length (parameter named lng)
    a positive integer width (parameter named wdth)

You will return an array with the size of each of the squares.

When the initial parameters are so that lng == wdth, the solution [lng] would 
be the most obvious but not in the spirit of this challengs so, in that case, 
the library returns None. 

	squaresInRect  5  3 should return Some [3,2,1,1]
	squaresInRect  3  5 should return Some [3,2,1,1]
	squaresInRect 20 14 should return Some [14, 6, 6, 2, 2, 2]
	squaresInRect 5 5 should return None


