using System.Collections.Generic;
using System.Linq;

public class DoubleLinear 
{
	
	public static int DblLinear (int n) 
	{
		var ss = new SortedSet<int> {1};
		
		for (int i = 0; i < n; ++i)
		{
			ss.Add(ss.First() * 3 + 1);
			ss.Add(ss.First() * 2 + 1);
			ss.Remove(ss.First());
		}
		
		return ss.First();
	}
}
