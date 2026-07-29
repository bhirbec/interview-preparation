# Check Balanced
# Difficulty: easy
# Tags: #tree #dfs #recursion
#
# You are given a binary tree. Implement a function to check whether it is
# balanced. For the purpose of this problem, a balanced tree is one in which the
# heights of the two subtrees of any node never differ by more than one.
#
# Input:
#   - A binary tree represented as nested dicts. A node is a dict that may hold a
#     'left' and/or 'right' key pointing to child nodes; an absent key means no
#     child. An empty dict {} is a leaf. None represents an empty tree.
# Output:
#   - True if the tree is height-balanced, otherwise False.
#
# Constraints:
#   - An empty tree is considered balanced.
#
# Examples:
#   is_balanced(None) -> True                      (empty tree)
#   is_balanced({})   -> True                      (single node)
#   is_balanced({'left': {'left': {}}}) -> False   (left height 2 vs right 0)
#   A full tree of depth 4 -> True
#
# Approach: a single post-order DFS returns each subtree's height, or -1 as a
# sentinel once any subtree is found unbalanced, so it short-circuits in O(n).

import unittest


def is_balanced(n):
  return check_depth(n) != -1


def check_depth(n):
  if n is None:
    return 0

  left = check_depth(n.get('left'))
  if left == -1:
    return -1

  right = check_depth(n.get('right'))
  if right == -1:
    return -1

  diff = abs(left - right)
  if diff > 1:
    return -1

  return max(left, right) + 1


class TestIsBalanced(unittest.TestCase):
  def test_empty_tree_is_balanced(self):
    self.assertTrue(is_balanced(None))

  def test_single_node_is_balanced(self):
    self.assertTrue(is_balanced({}))

  def test_balanced_full_tree(self):
    def full(depth):
      if depth == 0:
        return {}
      return {'left': full(depth - 1), 'right': full(depth - 1)}
    self.assertTrue(is_balanced(full(4)))

  def test_off_by_one_is_balanced(self):
    # Left subtree height 2, right subtree height 1: differ by exactly one.
    tree = {
        'left': {'left': {}, 'right': {}},
        'right': {'left': {}},
    }
    self.assertTrue(is_balanced(tree))

  def test_unbalanced_left_heavy(self):
    # Degenerate left chain of depth 2, no right subtree: unbalanced.
    tree = {'left': {'left': {}}}
    self.assertFalse(is_balanced(tree))

  def test_unbalanced_deep_in_subtree(self):
    tree = {
        'left': {},
        'right': {'right': {'right': {'right': {}}}},
    }
    self.assertFalse(is_balanced(tree))

  def test_balanced_with_single_child_each_side(self):
    tree = {'left': {}, 'right': {}}
    self.assertTrue(is_balanced(tree))


if __name__ == '__main__':
  unittest.main()
