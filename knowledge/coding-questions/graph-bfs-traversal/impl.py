# Breadth-First Search on an Adjacency List
#
# A graph is given as an adjacency list: a dict mapping each node to the list
# of nodes it has an edge to. Edges are directed as written, so an undirected
# graph appears with each edge listed from both ends.
#
#   {'a': ['b', 'c'], 'b': ['d'], 'c': [], 'd': []}
#
# Write breadth-first search over that structure.
#
#   bfs_order(graph, start)
#     Return the list of nodes reachable from `start`, in the order BFS visits
#     them: `start` first, then all of its neighbours, then everything one hop
#     further out, and so on. Within a level, follow the order the neighbours
#     appear in the adjacency list. Each node appears exactly once.
#
#   bfs_distances(graph, start)
#     Return a dict mapping every reachable node to its distance from `start`
#     counted in edges (`start` itself is 0).
#
# Both must raise KeyError when `start` is not a node of the graph. Nodes not
# reachable from `start` are simply left out of the result. The graph may
# contain cycles and self-loops, so mark a node as seen when you enqueue it,
# not when you dequeue it -- otherwise a node with two parents on the same
# level gets queued twice.
#
# A node listed as a neighbour but missing as a key is treated as having no
# outgoing edges.
#
# Complexity to aim for: O(V + E) time and O(V) space.
#
# Examples:
#   graph = {'a': ['b', 'c'], 'b': ['d'], 'c': ['d'], 'd': [], 'e': ['a']}
#   bfs_order(graph, 'a')      -> ['a', 'b', 'c', 'd']     ('e' is unreachable)
#   bfs_distances(graph, 'a')  -> {'a': 0, 'b': 1, 'c': 1, 'd': 2}
#   bfs_order(graph, 'd')      -> ['d']
#   bfs_order(graph, 'z')      -> raises KeyError
#
#   ring = {1: [2], 2: [3], 3: [1]}
#   bfs_order(ring, 1)         -> [1, 2, 3]


def bfs_order(graph, start):
  # TODO: implement
  raise NotImplementedError


def bfs_distances(graph, start):
  # TODO: implement
  raise NotImplementedError
