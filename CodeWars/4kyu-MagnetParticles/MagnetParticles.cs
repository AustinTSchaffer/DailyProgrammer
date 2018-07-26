using System;
using System.Linq;
using System.Collections.Generic;


public class Magnets 
{
	private static IEnumerable<int> Range(int start, int stop)
	{
		for (int i = start; i <= stop; ++i)
			yield return i;
	}
	
	private static double V (int k, int n)
	{
		double _k = (double) k;
		double _n = (double) n;
		
		return 1.0 / (_k * Math.Pow((_n + 1.0), (2.0 * _k)));
	}
	
	private static double U (int K, int N)
	{
		return Range(1, N).Sum(n => V(K, n));
	}
	
	public static double Doubles(int K, int N)
	{
		return Range(1, K).Sum(k => U(k, N));
	}
}
