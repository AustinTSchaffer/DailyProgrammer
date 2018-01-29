using System;
using System.Collections.Generic;
using System.Linq;

public class ConnectFour
{
	private static string[,] board;
	private static int[] columnNextPos;
	
	
	public static IEnumerable<int> IntRange(int offset, int count, int step)
	{
		for (int i = offset; i < offset + count; i += step)
			yield return i;
	}
	

	private static IEnumerable<string[]> GetAllConnectedFours(int col, int row)
	{   
		// Up to 4: Horizontals
		for (int colOffset = 0; colOffset <= board.GetLength(0) - 4; colOffset++)
		{
			var intRange = IntRange(colOffset, 4, 1);
			
			if (intRange.Contains(col))
			{
				var output = new string[4];
				foreach (int i in intRange)
				{
					output[i - colOffset] = board[i, row];
				}
				yield return output;
			}
		}
			   
		// Up to 3: Verticals
		for (int rowOffset = 0; rowOffset <= board.GetLength(1) - 4; rowOffset++)
		{
			var intRange = IntRange(rowOffset, 4, 1);
			
			if (intRange.Contains(row))
			{
				var output = new string[4];
				foreach (int i in intRange)
					output[i - rowOffset] = board[col, i];
				yield return output;
			}
			
		}
		
		for (int i = 0; i < 4; ++i)
		{
			var colRange_NWSE = IntRange(col - i, 4, 1).ToList(); 
			var rowRange_NWSE = IntRange(row - i, 4, 1).ToList();

			var colRange_SWNE = IntRange(col + i, 4, 1).ToList();
			var rowRange_SWNE = IntRange(row - i, 4, 1).ToList();
			
			if (!colRange_NWSE.Any(_i => _i < 0 || _i >= board.GetLength(0)) && !rowRange_NWSE.Any(_i => _i < 0 || _i >= board.GetLength(1)))
			{
				var output = new string[4];
				for (int j = 0; j < 4; ++j)
					output[j] = board[colRange_NWSE[j], rowRange_NWSE[j]];
				yield return output;
			}
			
			if (!colRange_SWNE.Any(_i => _i < 0 || _i >= board.GetLength(0)) && !rowRange_SWNE.Any(_i => _i < 0 || _i >= board.GetLength(1)))
			{
				var output = new string[4];
				for (int j = 0; j < 4; ++j)
					output[j] = board[colRange_SWNE[j], rowRange_SWNE[j]];
				yield return output;				
			}
			
		}
	}


	public static string WhoIsWinner(List<string> piecesPositionList)
	{
		board = new string[7, 6];
		columnNextPos = new int[7];
		
		foreach (var move in piecesPositionList)
		{
			var split = move.Split('_');
			
			int col = (int) (split[0][0] - 'A');
			int row = columnNextPos[col];
			
			board[col, row] = split[1];
			columnNextPos[col]++;

			bool winner = GetAllConnectedFours(col, row)
			  .Any(f => f.All(p => split[1].Equals(p, StringComparison.OrdinalIgnoreCase)));
			
			if (winner) return split[1];
		}
		
		return "Draw";
	}
}