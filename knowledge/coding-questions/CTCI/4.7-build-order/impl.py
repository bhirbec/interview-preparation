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


def build_order(projects, dependencies):
  # TODO: implement
  raise NotImplementedError
