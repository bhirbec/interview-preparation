# Check Subtree
#
# You are given two binary trees, T1 (large) and T2 (smaller). Determine
# whether T2 is a subtree of T1. T2 is a subtree of T1 if there exists a node n
# in T1 such that the subtree rooted at n is identical to T2 (same structure and
# same node values).
#
# Input: the roots n1 (T1) and n2 (T2), each a Node or None.
# Output: True if T2 is a subtree of T1, otherwise False.
#
# Convention: an empty T2 (n2 is None) is considered a subtree of any tree, so
# is_subtree returns True in that case.
#
# Examples:
#   T1 = 10(5(2(1,3),7(6,8)),15(12,41)), T2 = 15(12,41) -> True
#   T1 = 10(5,15), T2 = 5(1) -> False (5 in T1 is a leaf, not 5 with child 1)
#   T1 = any, T2 = None -> True
#   T1 = None, T2 = 15(12,41) -> False


class Node:
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right


def is_subtree(n1, n2):
  # TODO: implement
  raise NotImplementedError
