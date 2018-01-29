using System;
using System.Collections.Generic;

public class Kata{
	public static int getLoopSize(LoopDetector.Node startNode){
		
		var hashIndexDict = new Dictionary<LoopDetector.Node, int>();

		var count = 0;
		var currNode = startNode;
		
		
		while (!hashIndexDict.ContainsKey(currNode))
		{
			hashIndexDict.Add(currNode, count);
			currNode = currNode.next;
			count += 1;
		}
		
		return count - hashIndexDict[currNode];
	}
}
