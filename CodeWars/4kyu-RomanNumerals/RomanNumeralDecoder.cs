using System;
using System.Collections.Generic;

public class RomanDecode
{

	private static Dictionary<char, int> _numeralValueDict = new Dictionary<char, int>
	{
		{'\0', 0},
		{'I', 1},
		{'V', 5},
		{'X', 10},
		{'L', 50},
		{'C', 100},
		{'D', 500},
		{'M', 1000}
	};
	

	public static int Solution(string roman)
	{
		int sum = 0;
		
		for (int i = 0; i < roman.Length; ++i)
		{
			var currNumeral = roman[i];
			var nextNumeral = (i + 1 != roman.Length) ? roman[i + 1] : '\0';
			var numeralValue = _numeralValueDict[currNumeral];
			
			// If the next numeral has a higher value, it current numeral should be subtracted.
			sum += (_numeralValueDict[nextNumeral] > numeralValue) ? -numeralValue : numeralValue;
		}
		
		return sum;
	}
}