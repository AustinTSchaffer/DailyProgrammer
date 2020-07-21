import java.util.ArrayList;
import java.util.List;
import java.util.Stack;

/**
 * Solution to problem number 5.
 *
 * @author Austi
 * @since 19 May 2016
 */
public class YOLOTTL {

	/**
	 * List of nodes.
	 */
	private List<Node> graph = null;

	/**
	 * Constructor. Initializes data structures.
	 */
	public YOLOTTL() {
		this.graph = new ArrayList<Node>();
	}

	/**
	 * Adds a connection between two distinct nodes.
	 *
	 * @param aUID The UID of a Node.
	 * @param bUID The UID of a different Node.
	 * @return Reference to this YOLOTTL instance.
	 */
	public YOLOTTL addConnection(int aUID, int bUID) {
		
		if (aUID == bUID) return this; 
			
		Node nodeA = new Node(aUID);
		Node nodeB = new Node(bUID);

		if (!this.graph.contains(nodeA)) this.graph.add(nodeA);
		if (!this.graph.contains(nodeB)) this.graph.add(nodeB);
		
		nodeA = this.graph.get(this.graph.indexOf(nodeA));
		nodeB = this.graph.get(this.graph.indexOf(nodeB));

		nodeA.connect(nodeB);
		nodeB.connect(nodeA);

		return this;
	}


	/**
	 * Tests the number of nodes reachable from (uid) with (ttl) steps.
	 *
	 * @param uid UID of the starting node.
	 * @param ttl Distance from starting node.
	 * @return "(n | All) node(s) (un)reachable from node (uid) with TTL = (ttl)"
	 */
	public String testPacket(int uid, int ttl) {
		
		int startingIndex = this.graph.indexOf(new Node(uid));
		Node startingNode = (startingIndex < 0)? null : this.graph.get(startingIndex);
		List<Node> reachableNodes = this.findAllReachableNodes(startingNode, ttl);
		
		int diff = graph.size() - reachableNodes.size();
		
		return String.format("%s node%s %sreachable from node %d with TTL = %d", 
						(diff == 0 || diff == graph.size())? "All" : String.format("%d", diff),
						(diff == 1)? "" : "s",
						(diff == 0)? "" : "un",
						uid,
						ttl
						);
	}

	
	/**
	 * Finds all nodes reachable from a starting Node.
	 *
	 * @param startingNode Starting node.
	 * @param ttl Depth of search.
	 * @return List of all reachable nodes.
	 */
	private List<Node> findAllReachableNodes(Node startingNode, int ttl) {
		
		if (null == startingNode) return new ArrayList<Node>();
		
		List<Node> reachableNodes = new ArrayList<Node>();
		List<Node> fringe         = new ArrayList<Node>();
		List<Node> fringeBuffer   = new ArrayList<Node>();
		
		fringe.add(startingNode);

		for (ttl = ttl; ttl >= 0; --ttl) {

			reachableNodes.addAll(fringe);
			
			for (Node n1 : fringe) {
				for (Node n2 : n1.connections()) {
					if (!reachableNodes.contains(n2) && !fringeBuffer.contains(n2)) {
						fringeBuffer.add(n2);
					}
				}
			}

			fringe.clear();
			fringe.addAll(fringeBuffer);
			fringeBuffer.clear();
		}

		return reachableNodes;
	}


	/**
	 * Displays connection information
	 */
	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();

		for (Node n : this.graph) {
			sb.append("Node: " + n.getUID() + "\r\n");
			for (Node n2 : n.connections()) {
				sb.append("   + " + n2.getUID() + "\r\n");

			}

		}
		return sb.toString();

	}


	/**
	 * Encapsulates a network node an its connections to other nodes.
	 */
	class Node  {
		
		private int uid = 0;

		/**
		 * Hold pointers to other nodes.
		 */
		private List<Node> connections = null;

		/**
		 * Constructor.
		 *
		 * @param uid The unique identifying number of this Node.
		 */
		public Node(int uid) {
			this.uid = uid;
			this.connections = new ArrayList<Node>();
		}

		/**
		 * Returns the UID of this Node.
		 */
		public int getUID(){
			return this.uid;
		}

		/**
		 * Adds a 1-way connection from this node to another.
		 *
		 * @param node A different Node object.
		 * @return Returns a copy of this Node.
		 */
		public Node connect(Node node) {
			if (null != node && node != this && !this.connections.contains(node)) {
				this.connections.add(node);
			}
			return this;
		}

		
		/**
		 * Returns a list containing all of the Nodes connected to this Node.
		 * 
		 * Returned list is a copy of the internal list of connections.
		 *
		 * @return list of connected Node objects.
		 */
		public List<Node> connections() {
			List<Node> nodes = new ArrayList<Node>(this.connections);
			return nodes;
		}

		
		@Override
		public boolean equals(Object o) {
			return 
				o instanceof Node && 
				((Node) o).getUID() == this.getUID();
		}

		@Override
		public int hashCode() {
			return this.getUID();
		}
	}
}
