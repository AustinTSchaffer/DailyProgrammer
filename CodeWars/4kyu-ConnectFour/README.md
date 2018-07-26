# Connect Four (4 kyu)

You will receive a list of string that shows the order of the pieces which 
dropped in columns: 

```cs
List<string> myList = new List<string>()
{
	"A_Red",
	"B_Yellow",
	"A_Red",
	"B_Yellow",
	"A_Red",
	"B_Yellow",
	"G_Red",
	"B_Yellow"
};
```

The list may contains 42 strings or fewer, but the order shows the order that 
players are playing. 

The first player who connect four items in same color is the winner. 

The function should return "Yellow", "Red" or "Draw". 
