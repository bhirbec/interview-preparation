# Route Between Nodes
# Difficulty: medium
# Tags: #graph #bfs
#
# You are given a directed graph and two nodes. Write an algorithm to determine
# whether there is a route (a directed path) between the two nodes.
#
# Input:
#   - graph: an adjacency list mapping each node to the list of nodes it has an
#     outgoing edge to, e.g. {1: [2, 3], 2: [4], 3: [], 4: []}.
#   - origin: the start node.
#   - dest: the target node.
# Output:
#   - True if dest is reachable from origin by following directed edges (a node
#     is always reachable from itself), otherwise False.
#
# Constraints:
#   - Nodes may form cycles; visited bookkeeping prevents re-processing.
#
# Examples:
#   graph = {1: [2, 3], 2: [4, 3], 3: [], 4: [1, 5], 5: [2], 6: [5]}
#   exists_path(graph, 1, 5) -> True   (1 -> 2 -> 4 -> 5)
#   exists_path(graph, 5, 6) -> False  (no edge leads into 6)
#   exists_path(graph, 3, 3) -> True   (a node reaches itself)
#
# Approach: breadth-first search from origin, marking nodes visited to avoid
# cycling forever, returning True as soon as dest is dequeued.


def exists_path(graph, origin, dest):
  # TODO: implement
  raise NotImplementedError
