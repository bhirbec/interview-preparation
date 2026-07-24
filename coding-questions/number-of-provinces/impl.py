# Number of Provinces
#
# Difficulty: medium
# Tags: #graph #connected-components #dfs
#
# You are given the adjacency matrix of an undirected graph on `n` nodes,
# encoded as a list of `n` strings each of length `n`. `matrix[i][j] == '1'`
# means there is a direct edge between node i and node j, and '0' means there
# is not. The matrix is symmetric and `matrix[i][i] == '1'`.
#
# Two nodes belong to the same group if they are connected directly or
# indirectly (through a chain of edges). Return the number of connected
# components (groups).
#
# Constraints:
#   - 0 <= n, and every string has length n
#   - each character is '0' or '1'
#   - matrix[i][j] == matrix[j][i] (symmetric)
#
# Examples:
#   ["1100",                    -> 2   nodes {0,1,2} form one group (0-1, 1-2),
#    "1110",                          node 3 is alone
#    "0110",
#    "0001"]
#
#   ["10000",                   -> 5   identity matrix: every node is isolated
#    "01000",
#    "00100",
#    "00010",
#    "00001"]
#
#   ["110", "111", "011"]       -> 1   0-1 and 1-2 connect all three transitively
#   ["1"]                       -> 1
#   []                          -> 0
#
# Approach: treat each row index as a graph node and each '1' as an edge. Scan
# nodes; from each unvisited node run an iterative DFS over its row to mark the
# whole component visited, incrementing the group count once per component.

import unittest


def number_of_provinces(matrix):
  n = len(matrix)
  visited = set()
  groups = 0

  for start in range(n):
    if start in visited:
      continue

    groups += 1
    stack = [start]
    visited.add(start)

    while stack:
      node = stack.pop()
      for other in range(n):
        if matrix[node][other] == '1' and other not in visited:
          visited.add(other)
          stack.append(other)

  return groups


class TestNumberOfProvinces(unittest.TestCase):
  def test_source_example(self):
    self.assertEqual(number_of_provinces(['1100', '1110', '0110', '0001']), 2)

  def test_identity_all_isolated(self):
    matrix = ['10000', '01000', '00100', '00010', '00001']
    self.assertEqual(number_of_provinces(matrix), 5)

  def test_transitive_chain_is_one_group(self):
    self.assertEqual(number_of_provinces(['110', '111', '011']), 1)

  def test_single_node(self):
    self.assertEqual(number_of_provinces(['1']), 1)

  def test_empty(self):
    self.assertEqual(number_of_provinces([]), 0)

  def test_fully_connected(self):
    self.assertEqual(number_of_provinces(['111', '111', '111']), 1)

  def test_two_separate_pairs(self):
    matrix = ['1100', '1100', '0011', '0011']
    self.assertEqual(number_of_provinces(matrix), 2)

  def test_two_isolated_nodes(self):
    self.assertEqual(number_of_provinces(['10', '01']), 2)

  def test_two_connected_nodes(self):
    self.assertEqual(number_of_provinces(['11', '11']), 1)

  def test_last_node_bridges_two_halves(self):
    # 0-1 linked, 2-3 linked, and 4 links to both 1 and 2 -> all one group
    matrix = [
        '11001',
        '11001',
        '00111',
        '00111',
        '11111',
    ]
    self.assertEqual(number_of_provinces(matrix), 1)

  def test_component_discovered_from_later_index(self):
    # node 0 isolated; nodes 1,2,3 form a component reached only from index 1
    matrix = ['1000', '0110', '0111', '0011']
    self.assertEqual(number_of_provinces(matrix), 2)


if __name__ == '__main__':
  unittest.main()
