import java.util.ArrayList;

/**
 * Finds and generates strings of characters using a deprecated system
 * that maps certain single digit integers to groupings of characters.
 * 
 * @author austi
 *
 */
public class NumpadWordMatcher {

	
	public NumpadWordMatcher() {
		this.dictionary = new ArrayList<>();
		this.numpadEntries = new ArrayList<>();
	}
	
	
	private ArrayList<String> dictionary;
	private ArrayList<String> numpadEntries;
	
	
	/**
	 * Returns a list of strings containing all possible letter arrangements given
	 * a string of button presses. Any occurrences of 0 or 1 will be ignored, given that
	 * these keys have no associated letters. Implementation is recursive.
	 * 
	 * @param numbers A string of decimal digits, representing a dial pad input.
	 * @return A list containing all character strings that can be generated 
	 * using the input button presses.
	 */
	public ArrayList<String> getAllCombinations(String numbers) {
		
		// Verify that s is not empty and a number.
		if (null == numbers || numbers.length() == 0 || !numbers.matches("[0-9]+")) {
			ArrayList<String> baseCase = new ArrayList<String>();
			baseCase.add("");
			return baseCase;
		}
		
		ArrayList<String> recurSub  = this.getAllCombinations(numbers.substring(1));
		
		int firstNumber = (int) (numbers.charAt(0) - '0');
		if (firstNumber == 0 || firstNumber == 1) return recurSub;
		
		ArrayList<String> recurFull = new ArrayList<String>();
		
		
 		for (String lowerPartial : recurSub) {
			for (char c : NumpadWordMatcher.NUMPAD[firstNumber].toCharArray()) {
				recurFull.add(c + lowerPartial);
			}
		}
		
		return recurFull;
	}

	
	/**
	 * Adds an entry to the dictionary.
	 * @param entry Dictionary entry.
	 * @return Copy of this object for method chaining.
	 */
	public NumpadWordMatcher addDictionaryEntry(String entry) {
		if (null != entry && entry.length() > 0) {			
			this.dictionary.add(entry);
		}
		return this;
	}
	
	
	/**
	 * Adds a keystroke.
	 * @param keyStroke Typed, numeric keystroke.
	 * @return Copy of this object for method chaining.
	 */
	public NumpadWordMatcher addKeyStroke(String keyStroke) {
		if (null != keyStroke && keyStroke.length() > 0 && keyStroke.matches("[0-9]+")) {
			this.numpadEntries.add(keyStroke);
		}
		return this;
	}
	
	
	/**
	 * Outputs all entries from the dictionary that can be generated using any
	 * of the numberpad keystrokes. If none of the dictionary entries can be generated
	 * using the keystroke, then all possible keystrokes will be returned. Output will
	 * be sorted alphabetically.
	 * 
	 * @return Challenge output.
	 */
	public ArrayList<String> execute() {
		ArrayList<String> keyStrokePossiblilites = new ArrayList<String>();
		ArrayList<String> output = new ArrayList<String>();
		
		for (String keyStroke : this.numpadEntries) {
			keyStrokePossiblilites.addAll(this.getAllCombinations(keyStroke));
		}
		
		for (String entry : this.dictionary) {
			if (keyStrokePossiblilites.contains(entry)) {
				output.add(entry);
			}
		}
		
		output.sort(null);
		keyStrokePossiblilites.sort(null);
		
		return (output.size() > 0)? output : keyStrokePossiblilites;
	}
	
	
	/**
	 * Matches integers to their respective letters, as specified
	 * by the ITU E 1.161 International Standard.
	 */
	private static final String[] NUMPAD = new String[] {
			"",		// 0
			"",		// 1
			"ABC",	// 2
			"DEF",	// 3
			"GHI",	// 4
			"JKL",	// 5
			"MNO",	// 6
			"PQRS",	// 7
			"TUV",	// 8
			"WXYZ"	// 9
	};


}

