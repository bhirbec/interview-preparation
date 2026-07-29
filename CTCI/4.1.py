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

import unittest
from queue import Queue


def exists_path(graph, origin, dest):
  q = Queue()
  q.put(origin)
  visited = {}

  while not q.empty():
    n = q.get()
    if n in visited:
      continue

    if n == dest:
      return True

    for ni in graph[n]:
      q.put(ni)

    visited[n] = True

  return False


class TestExistsPath(unittest.TestCase):
  def setUp(self):
    self.graph = {
        1: [2, 3],
        2: [4, 3],
        3: [],
        4: [1, 5],
        5: [2],
        6: [5],
    }

  def test_path_exists_multi_hop(self):
    self.assertTrue(exists_path(self.graph, 1, 5))

  def test_direct_edge(self):
    self.assertTrue(exists_path(self.graph, 1, 2))

  def test_no_path(self):
    self.assertFalse(exists_path(self.graph, 5, 6))

  def test_node_reaches_itself(self):
    self.assertTrue(exists_path(self.graph, 3, 3))

  def test_cycle_terminates(self):
    # 1 -> 2 -> 3 -> 1 forms a cycle; searching within it must terminate.
    cyclic = {1: [2], 2: [3], 3: [1]}
    self.assertTrue(exists_path(cyclic, 1, 3))
    self.assertTrue(exists_path(cyclic, 3, 2))

  def test_single_node_graph(self):
    self.assertTrue(exists_path({1: []}, 1, 1))
    self.assertFalse(exists_path({1: [], 2: []}, 1, 2))


if __name__ == '__main__':
  unittest.main()
