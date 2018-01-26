using System;
using System.Text;
using System.Collections.Generic;

public static class RomanNumeralEncoder
{
	private static int ProcessNumeralRange(this int n, int minimum, string nums, StringBuilder builder)
	{
		builder.Append(new String(nums[0], n / minimum)
			.Replace(new String(nums[0], 5), $"{nums[1]}")
			.Replace(new String(nums[0], 4), $"{nums[0]}{nums[1]}")
			.Replace($"{nums[1]}{nums[0]}{nums[1]}", $"{nums[0]}{nums[2]}"));

		return n % minimum;
	}


	public static string Solution(int n)
	{
		var builder = new StringBuilder();
	
		n.ProcessNumeralRange(1000, "M\0\0", builder)
			.ProcessNumeralRange(100, "CDM", builder)
			.ProcessNumeralRange(10, "XLC", builder)
			.ProcessNumeralRange(1, "IVX", builder);
	
		return builder.ToString();
	}
}
