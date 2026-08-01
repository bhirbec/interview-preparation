# Union-Find with Union by Rank and Path Compression
#
# Implement a disjoint-set (union-find) structure over the integers
# 0, 1, ..., n-1. Every element starts in its own set; `union` merges two sets
# and `find` reports which set an element belongs to.
#
# Represent each set as a tree of parent pointers whose root is the set's
# representative, and apply both classic optimisations:
#
#   - union by rank: when merging, hang the shorter tree under the taller one,
#     so trees stay shallow. Only when the two ranks are equal does the
#     surviving root's rank grow by one.
#   - path compression: while walking up to the root inside find(), re-point
#     every node on the path directly at the root.
#
# Together they make the amortised cost of find/union effectively constant.
#
# Required API:
#   UnionFind(n)      - n singleton sets; ValueError if n is negative
#   find(x)           - the representative of x's set; IndexError when x is not
#                       in [0, n)
#   union(x, y)       - merge the sets of x and y; return True if they were
#                       separate and got merged, False if they were already in
#                       the same set
#   connected(x, y)   - True when x and y are in the same set
#   count()           - number of disjoint sets remaining
#   size(x)           - number of elements in x's set
#
# Examples:
#   uf = UnionFind(5)
#   uf.count()                    -> 5
#   uf.connected(0, 1)            -> False
#   uf.union(0, 1)                -> True
#   uf.union(1, 0)                -> False   (already together)
#   uf.connected(0, 1)            -> True
#   uf.count()                    -> 4
#   uf.size(0)                    -> 2
#   uf.union(2, 3); uf.union(1, 2)
#   uf.connected(0, 3)            -> True
#   uf.count(), uf.size(3)        -> 2, 4    (element 4 is still alone)


class UnionFind:
  def __init__(self, n):
    # TODO: implement
    raise NotImplementedError

  def find(self, x):
    # TODO: implement
    raise NotImplementedError

  def union(self, x, y):
    # TODO: implement
    raise NotImplementedError

  def connected(self, x, y):
    # TODO: implement
    raise NotImplementedError

  def count(self):
    # TODO: implement
    raise NotImplementedError

  def size(self, x):
    # TODO: implement
    raise NotImplementedError
