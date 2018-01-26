using System;

public class Kata
{
	public static string MixedFraction(string s)
	{
		if (string.IsNullOrWhiteSpace(s)) throw new ArgumentException(nameof(s));

		var split = s.Split('/');
		
		int numer = 0; Int32.TryParse(split[0], out numer);
		int denom = 0; Int32.TryParse(split[1], out denom);
		if (denom == 0) throw new DivideByZeroException();

		var sign = Math.Sign(numer) * Math.Sign(denom) < 0 ? "-" : "";
		
		int wholeNumber = numer / denom;
		numer = Math.Abs(numer % denom);
		denom = Math.Abs(denom);
		
		int gcd = GCD(numer, denom);
		numer /= gcd;
		denom /= gcd;
		
		return 
			(numer == 0) ? $"{wholeNumber}" :
			(wholeNumber != 0) ? $"{wholeNumber} {numer}/{denom}" :
			$"{sign}{numer}/{denom}";
	}
	
	
	private static int GCD(int a, int b)
	{
		while (b != 0)
		{
			int t = b;
			b = a % b;
			a = t;
		}
		
		return a;
	}
}