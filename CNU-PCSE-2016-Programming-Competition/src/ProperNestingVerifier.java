import java.util.LinkedList;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Checks an HTML string for proper nesting and closing of HTML tags.
 * 
 * @author austi
 *
 */
public class ProperNestingVerifier {
	
	
	/**
	 * HTML tags where closing tags are optional.
	 */
	static final String[] SINGLETON_TAGS = new String[] {
			"input",
			"doctype",
			"br",
			"img",
			"hr",
			"basefont",
			"meta",
			"link"
	};
	
	
	/** 
	 * '<'
	 * optional whitespace
	 * optional '/'
	 * optional whitespace
	 * letters
	 * optional whitespace
	 * optional extras
	 * '>'
	 */
	private static final Pattern HTML_TAG_PATTERN = Pattern.compile("<\\s*/?\\s*[a-zA-Z]+\\s*[^>]*>");
	
	
	/** 
	 * '<'
	 * optional whitespace
	 * letters
	 * optional whitespace
	 * optional extras
	 * '>'
	 */
	private static final Pattern OPEN_TAG_PATTERN  = Pattern.compile("<\\s*[a-zA-Z]+\\s*[^>]*>");
	
	
	/** 
	 * '<'
	 * optional whitespace
	 * '/'
	 * optional whitespace
	 * letters
	 * optional whitespace
	 * optional extras
	 * '>'
	 */
	private static final Pattern CLOSE_TAG_PATTERN = Pattern.compile("<\\s*/\\s*[a-zA-Z]+\\s*[^>]*>");
	
	
	/**
	 * Verifies a line of HTML to ensure that tags are closed correctly.
	 * 
	 * @param html A string that may contain HTML tags. Input must end with a '#'.
	 * @return 'VALID' if valid, 'Expected {0}, found {1}' if invalid.
	 */
	public static String verify(String html) {
		
		Stack<Tag> htmlTagStack = new Stack<Tag>();
		htmlTagStack.push(new Tag("#", true));
		
		LinkedList<Tag> htmlTagQueue = ProperNestingVerifier.getHTMLTags(html);

		Tag t;
		while (null != (t = htmlTagQueue.poll())) {
			if (t.isOpenTag && !t.isSingleton()) {
				htmlTagStack.push(t);
			}
			else if (!t.isOpenTag && !t.isSingleton()) {
				Tag t1 = htmlTagStack.pop();
				if (!t1.name.toLowerCase().equals(t.name.toLowerCase())) {
					return "Expected " + new Tag(t1.name, false).toString() + ", found " + t.toString();
				}
			}
		}
		
		
		return "VALID";
	}
	
	
	/**
	 * Returns all HTML tags found in html.
	 * 
	 * @param html A string that may contain HTML tags. Input must end with a '#'.
	 * @return A queue, representing all contained HTML tags in order of appearance.
	 */
	private static LinkedList<Tag> getHTMLTags(String html) {
		
		if (null == html || html.length() <= 0) {
			return new LinkedList<Tag>();			
		}
		
		Matcher m = HTML_TAG_PATTERN.matcher(html);
		LinkedList<Tag> tags = new LinkedList<Tag>();
		
		while (m.find()) {
			String tagString = m.group();
			
			int tagNameStartIndex = 0;
			int tagNameEndIndex = 0;
			for (int i = 0; i < tagString.length(); ++i) {
				
				char c = tagString.charAt(i);
				boolean charIsLetter = 
						Character.getType(c) == Character.UPPERCASE_LETTER ||
						Character.getType(c) == Character.LOWERCASE_LETTER;
				
				if (0 == tagNameEndIndex) {
					if (charIsLetter) {
						tagNameStartIndex = i;
						tagNameEndIndex = 1;
					}
				}
				else if (!charIsLetter) {
					tagNameEndIndex = i;
					break;
				}
			}
			
			tags.offer(new Tag(
					tagString.substring(tagNameStartIndex, tagNameEndIndex),
					OPEN_TAG_PATTERN.matcher(tagString).matches()
					));
		}
		
		tags.offer(new Tag("#", false));
		return tags;
	}


	
	/**
	 * Used to itemize the valid HTML tags found in an input string.
	 */	
	private static class Tag {
		
		public String name;
		public boolean isOpenTag;
		
		public Tag(String name, boolean isOpenTag) {
			this.name = name;
			this.isOpenTag = isOpenTag;
		}
		
		public boolean isSingleton() {
			for (String s : SINGLETON_TAGS) {
				if (s.toLowerCase().equals(name.toLowerCase())) {
					return true;
				}
			}
			return false;
		}
	
		@Override
		public String toString() {
			
			if (this.name.equals("#")) return name;
			
			return String.format("<%s%s>", this.isOpenTag? "" : "/", this.name);
		}
	}
}
