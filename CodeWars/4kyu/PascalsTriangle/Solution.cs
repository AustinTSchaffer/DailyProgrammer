using System;
using System.Collections.Generic;
using System.Linq;

public static class Kata
{
	private static List<int> _linearPascal = new List<int> { 1 };
	private static List<int> _lastRow = new List<int> { 1 };
	private static int _currentRow = 1;
	
	
	// Calculates and caches Pascal data 
	private static void PopulateInternalLinearPascal(int row)
	{
		while (_currentRow < row)
		{
			var newRow = new List<int>();
			
			newRow.Add(1);
			
			if (_currentRow > 1)
				for (int i = 1; i < _lastRow.Count; ++i)
					newRow.Add(_lastRow[i-1] + _lastRow[i]);
			
			newRow.Add(1);
			
			_linearPascal.AddRange(newRow);
			_lastRow.Clear();
			_lastRow = newRow;
			_currentRow++;
		}
	}


	public static List<int> PascalsTriangle(int n) {

		PopulateInternalLinearPascal(n);

		// Closed form sum of integers up to n
		// Equal to number of elements in triangle up through row n
		int numElements = (n * (n + 1)) / 2;
		return _linearPascal.Take(numElements).ToList();
	}
}
