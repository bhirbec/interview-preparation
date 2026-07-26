# Validate BST
# Difficulty: medium
# Tags: #tree #binary-search-tree #dfs #recursion
#
# You are given a binary tree. Implement a function to check whether it is a
# binary search tree: for every node, all values in its left subtree are less
# than the node's value and all values in its right subtree are greater.
#
# Input:
#   - The root Node of a binary tree (or None). Each Node has .value, .left and
#     .right. Values are distinct.
# Output:
#   - True if the tree satisfies the BST property, otherwise False.
#
# Constraints:
#   - An empty tree is a valid BST.
#   - Equal values are treated as violating the ordering (strict BST).
#
# Examples:
#   valid:   root 10, left subtree (5: 2,7), right subtree (15: 12,41) -> True
#   invalid: root 10 with a right-subtree node 6 (< 10)               -> False
#   is_bst(None)            -> True
#   is_bst(Node(1))         -> True
#
# Approach: recurse carrying an open (min, max) bound for each node; a node is
# valid only if min < value < max, then tighten the bound for each child. This
# catches violations that a naive parent-only comparison would miss.

import unittest


class Node():
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right


def is_bst(n):
  def _f(n, min_val, max_val):
    if n is None:
      return True

    if (min_val is not None and n.value <= min_val) or \
       (max_val is not None and n.value >= max_val):
      return False

    return _f(n.left, min_val, n.value) and _f(n.right, n.value, max_val)

  return _f(n, None, None)


def _valid_tree():
  return Node(
      value=10,
      left=Node(
          value=5,
          left=Node(value=2, left=Node(1), right=Node(3)),
          right=Node(value=7, left=Node(6), right=Node(8)),
      ),
      right=Node(
          value=15,
          left=Node(12),
          right=Node(41),
      ),
  )


class TestIsBst(unittest.TestCase):
  def test_empty_tree_is_valid(self):
    self.assertTrue(is_bst(None))

  def test_single_node_is_valid(self):
    self.assertTrue(is_bst(Node(1)))

  def test_valid_bst(self):
    self.assertTrue(is_bst(_valid_tree()))

  def test_left_child_greater_than_root(self):
    self.assertFalse(is_bst(Node(5, left=Node(6), right=Node(7))))

  def test_right_child_less_than_root(self):
    self.assertFalse(is_bst(Node(5, left=Node(3), right=Node(4))))

  def test_violation_deep_in_right_subtree(self):
    # 6 is a valid child of 15 locally but violates the root bound (< 10).
    tree = Node(
        value=10,
        left=Node(5),
        right=Node(15, left=Node(6), right=Node(20)),
    )
    self.assertFalse(is_bst(tree))

  def test_duplicate_value_is_invalid(self):
    self.assertFalse(is_bst(Node(5, left=Node(5))))

  def test_left_skewed_valid(self):
    self.assertTrue(is_bst(Node(3, left=Node(2, left=Node(1)))))


if __name__ == '__main__':
  unittest.main()
