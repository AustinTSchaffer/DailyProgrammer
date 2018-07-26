using System;
using System.Linq;
using System.Collections.Generic;

public class ConwayLife
{
	private class LivingCell
	{
		public int X { get; set; }
		public int Y { get; set; }
	}
  
	/* Please note that the htmlize function for C# currently isn't working
		properly. I tested it on rextester.com and the code worked as expected,
		but for some reason on codewars it isn't. When I find a solution to
		the issue I will update the function. */
	public static int[,] GetGeneration(int[,] cells, int generation)
	{
	  
		var oddAndEvenGenerations = new List<LivingCell>[] { new List<LivingCell>(), new List<LivingCell>() };
  
  
		foreach (int x in Enumerable.Range(0, cells.GetLength(0)))
			foreach (int y in Enumerable.Range(0, cells.GetLength(1)))
				if (cells[x, y] != 0)
					oddAndEvenGenerations[0].Add(new LivingCell() { X = x, Y = y });
		
		
		foreach (int gen in Enumerable.Range(0, generation))
		{
			var currentGeneration = oddAndEvenGenerations[gen % 2];
			var nextGeneration = oddAndEvenGenerations[(gen + 1) % 2];
			
			if (currentGeneration.Count == 0) return new int[0, 0];
			
			nextGeneration.Clear();
			
			var minX = currentGeneration.Select(c => c.X).Min();
			var minY = currentGeneration.Select(c => c.Y).Min();
			
			var maxX = currentGeneration.Select(c => c.X).Max();
			var maxY = currentGeneration.Select(c => c.Y).Max();
			
			foreach (int x in Enumerable.Range(minX - 1, maxX - minX + 3))
			foreach (int y in Enumerable.Range(minY - 1, maxY - minY + 3))
			{
				var currentCellAlive = currentGeneration
					.Where(c => (c.X == x && c.Y == y))
					.Any();
				
				var numNeighbors = currentGeneration
					.Where(c => c.X == x-1 || c.X == x || c.X == x+1)
					.Where(c => c.Y == y-1 || c.Y == y || c.Y == y+1)
					.Where(c => !(c.X == x && c.Y == y))
					.Take(4)
					.Count();
				
				var live = (currentCellAlive && (numNeighbors == 2)) || numNeighbors == 3;
				
				if (live) nextGeneration.Add(new LivingCell() { X = x - minX, Y = y - minY });
			}
		}
		
		var outputGeneration = oddAndEvenGenerations[generation % 2];
		var outputGeneration2dArray = FormatCellsAs2dArray(outputGeneration);
		return outputGeneration2dArray;
	}
	
	
	private static int[,] FormatCellsAs2dArray(List<LivingCell> generation)
	{
		var minX = generation.Select(c => c.X).Min();
		var minY = generation.Select(c => c.Y).Min();
		
		var maxX = generation.Select(c => c.X).Max();
		var maxY = generation.Select(c => c.Y).Max();
		
		var output = new int[((maxX - minX) + 1), ((maxY - minY) + 1)];
		
		foreach (var cell in generation)
			output[cell.X - minX, cell.Y - minY] = 1;
		
		return output;
	}
	
	
	private static void PrintGeneration(int[,] generation)
	{
		foreach (int x in Enumerable.Range(0, generation.GetLength(0)))
		{
			foreach (int y in Enumerable.Range(0, generation.GetLength(1)))
			{
				Console.Write(generation[x, y]);
			}
			Console.WriteLine();
	   }
	}
}