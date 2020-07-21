import java.util.regex.Pattern;

/**
 * Solution to Problem Number 1.
 * 
 * @author austi
 * @since 26 April 2016
 */
public class ExcellentParser {


	/**
	 * Parses one input.
	 * 
	 * Example Inputs: 
	 * R1C1          --> A1
	 * R3C1          --> A3
	 * R1C3          --> C1
	 * R2999999C26 --> Z2999999
	 * R52C52        --> AZ52
	 * R53C17576     --> YYZ53
	 * R53C17602     --> YZZ53
	 * R0C0          --> 
	 * 
	 * @param input Input consists of lines of the form: RnCm. n represents 
	 * the row number [1, 300000000] and m represents the column number,
	 * 1 ≤ m ≤ 300000000. The values n and m define a single cell 
	 * on the spreadsheet. Input terminates with the line: R0C0 
	 * (that is, n and m are 0). There will be no leading zeroes
	 * or extra spaces in the input.
	 * 
	 * @return Given a single input line, this method will print out the
	 * appropriate cell address for the specified cell as described above.
	 */
	public static String parse(String input) {
		 
		if (null == input || !Pattern.matches("R\\d++C\\d++", input)) {
			return "";
		}

		// Output row is pulled directly from the input
		String outRowString = input.split("C")[0].substring(1);
		
		// Column number is pulled 
		String colString = input.split("C")[1];
		int colNum = Integer.parseInt(colString);
		String outColString = "";
		
	    while (colNum > 0) {
	    	colNum--;
	    	int remainder = colNum % 26;
	    	char digit = (char) (remainder + 'A');
	    	outColString = digit + outColString;
	    	colNum = (colNum - remainder) / 26;
	    }
		
		return outColString + outRowString;
	}

}
