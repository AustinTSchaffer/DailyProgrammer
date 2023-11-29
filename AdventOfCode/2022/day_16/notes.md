# Notes

One optimization strategy that we could employ for this would be to use something called the
"floyd warshall" algorithm to convert the input graph into a fully-connected graph, with edges
weighted by the minimum number of moves required to reach each node from any other node. Once
generated, we could also then delete all nodes from this view of the graph that have a value
of 0 (with the exception of the starting node). This should increase the number of possible
edges that can be traversed, but decrease the number of nodes that need to be visited.

One other optimization could be to adjust the value of each node as we move through the graph.
Essentially, each node as an apparent value of its flow rate, times the number of moves remaining
after the valve is turned. We can think of this as the "reward" of reaching a specific node.
However, redeeming the reward of a node causes the rewards of all other nodes to decrease. Can
we optimize the graph search by maximizing the redeemed rewards while minimizing the "lost"
rewards?


