# Build Order
# Difficulty: hard
# Tags: #graph #topological-sort #dfs #recursion
#
# You are given a list of projects and a list of dependencies. Each dependency
# is a pair (a, b) meaning project a must be built BEFORE project b. Find a
# valid build order: an ordering of all the projects such that, for every
# dependency (a, b), a appears before b. If no valid build order exists (the
# dependencies contain a cycle), signal an error.
#
# Input:
#   - projects: an iterable of hashable project identifiers.
#   - dependencies: an iterable of (a, b) pairs; a must come before b.
# Output:
#   - A list containing every project exactly once, in an order that satisfies
#     all dependencies, OR the string 'ERROR' if a cycle makes ordering
#     impossible.
#
# Note: several valid orderings may exist. Any ordering that respects every
# dependency is correct.
#
# Examples:
#   projects = ['a', 'b', 'c', 'd', 'e', 'f']
#   dependencies = [('a', 'd'), ('f', 'b'), ('b', 'd'), ('f', 'a'), ('d', 'c')]
#   -> e.g. ['e', 'f', 'b', 'a', 'd', 'c'] (a before d, f before b, ...)
#
#   projects = ['a', 'b'], dependencies = [('a', 'b'), ('b', 'a')]
#   -> 'ERROR' (cycle)
#
#   projects = ['a'], dependencies = [] -> ['a']
#
# Approach: DFS-based topological sort. Track nodes currently on the recursion
# stack to detect cycles; emit each node after all of its successors (reverse
# post-order) to obtain a valid build order.

import unittest


def build_order(projects, dependencies):
  adjacency_list = _build_adjacency_list(projects, dependencies)
  projects = list(projects)
  n = len(projects)
  order: list = [None] * n
  visited = {}
  visiting = {}
  index = n - 1

  def _dfs(p):
    nonlocal index
    if p in visiting:
      # we're currently visiting this node which means that we're in a cycle
      return False

    if p in visited:
      return True

    visiting[p] = True
    for p1 in adjacency_list[p]:
      if not _dfs(p1):
        return False

    visited[p] = visiting.pop(p)
    order[index] = p
    index -= 1
    return True

  for p in projects:
    if p not in visited:
      if not _dfs(p):
        return 'ERROR'

  return order


def _build_adjacency_list(projects, dependencies):
  adjacency_list = dict((p, []) for p in projects)
  for dep, p in dependencies:
    adjacency_list[dep].append(p)
  return adjacency_list


class TestBuildOrder(unittest.TestCase):
  def _assert_valid_order(self, projects, dependencies, order):
    # every project appears exactly once
    self.assertEqual(sorted(order), sorted(projects))
    # every dependency (a, b) has a before b
    position = {p: i for i, p in enumerate(order)}
    for a, b in dependencies:
      self.assertLess(
          position[a], position[b],
          msg='%r should come before %r in %r' % (a, b, order))

  def test_canonical_example(self):
    projects = ['a', 'b', 'c', 'd', 'e', 'f']
    dependencies = [('a', 'd'), ('f', 'b'), ('b', 'd'), ('f', 'a'), ('d', 'c')]
    order = build_order(projects, dependencies)
    self._assert_valid_order(projects, dependencies, order)

  def test_single_project_no_dependencies(self):
    self.assertEqual(build_order(['a'], []), ['a'])

  def test_no_dependencies(self):
    projects = ['a', 'b', 'c']
    order = build_order(projects, [])
    self.assertEqual(sorted(order), ['a', 'b', 'c'])

  def test_linear_chain(self):
    projects = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('b', 'c'), ('c', 'd')]
    order = build_order(projects, dependencies)
    self.assertEqual(order, ['a', 'b', 'c', 'd'])

  def test_direct_cycle(self):
    self.assertEqual(build_order(['a', 'b'], [('a', 'b'), ('b', 'a')]), 'ERROR')

  def test_indirect_cycle(self):
    projects = ['a', 'b', 'c']
    dependencies = [('a', 'b'), ('b', 'c'), ('c', 'a')]
    self.assertEqual(build_order(projects, dependencies), 'ERROR')

  def test_self_cycle(self):
    self.assertEqual(build_order(['a'], [('a', 'a')]), 'ERROR')

  def test_disconnected_components(self):
    projects = ['a', 'b', 'c', 'd']
    dependencies = [('a', 'b'), ('c', 'd')]
    order = build_order(projects, dependencies)
    self._assert_valid_order(projects, dependencies, order)


if __name__ == '__main__':
  unittest.main()
