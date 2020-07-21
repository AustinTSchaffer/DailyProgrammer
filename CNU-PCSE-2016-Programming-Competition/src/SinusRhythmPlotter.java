import java.util.ArrayList;

/**
 * Plots a series of triangle waves, given an amplitude and a string of characters.
 * 
 * @author austi
 * @since 28 April 2016
 */
public class SinusRhythmPlotter {

	
	private ArrayList<Wave> waves;
	private char[][] graph;
	
	
	/**
	 * Default no args constructor for initializing data structures.
	 */
	public SinusRhythmPlotter() {
		this.waves = new ArrayList<Wave>();
	}
	
	/**
	 * Adds a wave to the diagram.
	 * 
	 * @param amplitude The amplitude of the 
	 * @param line The string of characters that will be transformed into a waveform.
	 */
	public SinusRhythmPlotter addWave(int amplitude, String line) {
		this.waves.add(new Wave(amplitude, line));
		return this;
	}
	
	
	/**
	 * Prints all added waves to a single axis. This method will throw a NullPointerException if 
	 * it is called before the build() method.
	 * 
	 * @return String representation of the ASCII representation of the graph of triangle waves.
	 */
	@Override
	public String toString() {
		
		if (null == this.graph) {
			throw new NullPointerException("Graph was not initialized. Please call build() before toString()");
		}
		
		StringBuilder sb = new StringBuilder();
		for (char[] line : graph) {
			sb.append(line);
			sb.append(System.getProperty("line.separator"));
		}
		return sb.toString();
	}
	
	
	/**
	 * Wave information storage structure.
	 * 
	 * @author austi
	 */
	private class Wave {
		
		public Wave(int amplitude, String line) {
			this.amplitude = amplitude;
			this.line = (null == line)?
					"" : 
					String.copyValueOf(line.toCharArray());
		}
		
		public String line;
		public int amplitude;
	}

	/**
	 * Combines the wave information into a char[][] representation of a graph and 
	 * stores the result as a a member. The result can be viewed using the toString() 
	 * method. 
	 * 
	 * @return Returns this, so that toString() can be chained.
	 */
	public SinusRhythmPlotter build() {
		int maxAmp = 0;
		int maxLen = 0;
		
		for (Wave w : waves) {
			if (0 == w.amplitude) continue;
			
			maxAmp = (w.amplitude > maxAmp)? 
						w.amplitude : 
						maxAmp;
			maxLen = (w.line.length() > maxLen)? 
						w.line.length() : 
						maxLen;
		}
		
		// Nothing to draw?
		if (0 == maxAmp || 0 == maxLen) {
			this.graph = new char[0][0];
			return this;
		}
		
		// Set graph size to fit all characters.
		this.graph = new char[(maxAmp * 2) - 1][maxLen];
		int xAxis = maxAmp - 1;
		
		// Populate the empty graph with spaces.
		for (int i = 0; i < (maxAmp * 2) - 1; ++i)
			for (int j = 0; j < maxLen; ++j)
				graph[i][j] = ' ';
		
		// For each stored wave
		for (Wave w : waves) {
			
			// amp of 0 means no wave.
			if (0 == w.amplitude) continue;
			
			// Next height to draw a character (relative to xAxis)
			int nextPointHeight = 0;
			
			// Draw direction flipped due to zero index being top-left
			// An amplitude of 1 effectively redraws the xAxis.
			int drawDirection = 
					(w.amplitude == 1)? 0 :
					(w.amplitude > 0 )? -1 : 
					1;
			
			// Inverts the draw direction right before nextPointHeight
			// is w.amplitude away from xAxis.
			for (int i = 0; i < w.line.length(); i += 1) {
				graph[xAxis + nextPointHeight][i] = w.line.charAt(i);
				drawDirection *= ((Math.abs(nextPointHeight) + 1 >= Math.abs(w.amplitude))? -1 : 1);
				nextPointHeight += drawDirection;
			}
		}
		
		return this;
	}
}
