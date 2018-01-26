using System;

namespace HammingDistance
{
	
	public class Kata
	{
		public int HammingDistance(int a, int b){
			string _a = Convert.ToString(a, 2).PadLeft(32, '0');
			string _b = Convert.ToString(b, 2).PadLeft(32, '0');
    		
			var output = 0;
    		
			for (int i = 0; i < 32; ++i) {
				if (_a[i] != _b[i]) output++;
			}

    		return output;
		}
	}
}
