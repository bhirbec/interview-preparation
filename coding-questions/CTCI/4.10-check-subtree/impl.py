# Check Subtree
# Difficulty: medium
# Tags: #tree #recursion #dfs
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
#
# Approach: an identical subtree must have the same depth as T2. Walk T1 while
# computing each node's subtree depth; only when a node's depth equals T2's
# depth do we run a full structural comparison against T2.

import unittest


class Node:
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right


def is_subtree(n1, n2):
  if n2 is None:
    return True

  d2 = get_depth(n2)

  def f(n):
    if n is None:
      return 0, False

    left, r = f(n.left)
    if r:
      return left, r

    right, r = f(n.right)
    if r:
      return right, r

    d = max(left, right) + 1
    if d == d2:
      return d, compare_tree(n, n2)

    return d, False

  return f(n1)[1]


def get_depth(n):
  if n is None:
    return 0

  left = get_depth(n.left)
  right = get_depth(n.right)
  return max(left, right) + 1


def compare_tree(n1, n2):
  if n1 is None or n2 is None:
    # equal only if both are absent
    return n1 is None and n2 is None

  return (
      n1.value == n2.value
      and compare_tree(n1.left, n2.left)
      and compare_tree(n1.right, n2.right)
  )


def _big_tree():
  return Node(
      value=10,
      left=Node(
          value=5,
          left=Node(value=2, left=Node(value=1), right=Node(value=3)),
          right=Node(value=7, left=Node(value=6), right=Node(value=8)),
      ),
      right=Node(value=15, left=Node(value=12), right=Node(value=41)),
  )


class TestCheckSubtree(unittest.TestCase):
  def test_subtree_present(self):
    n1 = _big_tree()
    n2 = Node(value=15, left=Node(value=12), right=Node(value=41))
    self.assertTrue(is_subtree(n1, n2))

  def test_deep_subtree_present(self):
    n1 = _big_tree()
    n2 = Node(value=2, left=Node(value=1), right=Node(value=3))
    self.assertTrue(is_subtree(n1, n2))

  def test_leaf_subtree_present(self):
    n1 = _big_tree()
    self.assertTrue(is_subtree(n1, Node(value=8)))

  def test_root_equals_whole_tree(self):
    n1 = _big_tree()
    n2 = _big_tree()
    self.assertTrue(is_subtree(n1, n2))

  def test_value_mismatch(self):
    n1 = _big_tree()
    n2 = Node(value=15, left=Node(value=12), right=Node(value=99))
    self.assertFalse(is_subtree(n1, n2))

  def test_structure_mismatch(self):
    # 5 in T1 has two children; here T2's 5 has only a left child.
    n1 = _big_tree()
    n2 = Node(value=5, left=Node(value=2))
    self.assertFalse(is_subtree(n1, n2))

  def test_missing_value(self):
    n1 = _big_tree()
    self.assertFalse(is_subtree(n1, Node(value=100)))

  def test_empty_t2_is_subtree(self):
    self.assertTrue(is_subtree(_big_tree(), None))

  def test_empty_t1_non_empty_t2(self):
    self.assertFalse(is_subtree(None, Node(value=1)))

  def test_both_empty(self):
    self.assertTrue(is_subtree(None, None))


if __name__ == '__main__':
  unittest.main()
