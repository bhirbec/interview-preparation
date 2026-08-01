# Isomorphic Trees
#
# Two binary trees are isomorphic if one can be obtained from the other by
# swapping the left and right children of any number of nodes (any nodes, at any
# levels). Given the roots of two binary trees, return True if they are
# isomorphic and False otherwise. Two empty trees are isomorphic.
#
# Each node is a `Node` with a `data` value and optional `left` / `right`
# children.
#
# Constraints:
#   - Either root may be None (empty tree).
#   - Node values are comparable with ==.
#
# Examples:
#   root(12; L=15, R=17) and root(12; L=17, R=15) -> True   (children swapped)
#   root(12; L=15, R=17) and root(12; L=15, R=16) -> False  (value mismatch)
#   both empty (None, None)                       -> True
#   one empty, one non-empty                      -> False


class Node:
  def __init__(self, data, left=None, right=None):
    self.data = data
    self.left = left
    self.right = right


def is_isomorphic(a, b):
  # TODO: implement
  raise NotImplementedError
