# Minimal Tree
# Difficulty: easy
# Tags: #tree #binary-search-tree #recursion #array
#
# You are given a sorted (increasing order) array with unique integer elements.
# Write an algorithm to create a binary search tree of minimal height.
#
# Input:
#   - array: a list of distinct integers sorted in increasing order.
# Output:
#   - The root Node of a binary search tree whose height is minimal. Each Node
#     has .value, .left and .right. An empty array yields None.
#
# Constraints:
#   - Elements are unique and already sorted.
#
# Examples:
#   make_bst([])        -> None
#   make_bst([1])       -> Node(value=1)
#   make_bst([1, 2, 3]) -> root 2, left 1, right 3   (height 2)
#   make_bst([1, 2, 3, 4, 5, 6, 7]) -> height 3
#
# Approach: recursively pick the middle element of the current range as the
# subtree root so the two halves are balanced, giving minimal height.

import unittest


class Node(object):
  def __init__(self, left, right, value):
    self.left = left
    self.right = right
    self.value = value


def make_bst(array):
  n = len(array)
  return _make_bst(array, 0, n - 1)


def _make_bst(array, i, j):
  n = j - i
  if n < 0:
    return None

  mid = i + n // 2
  left = _make_bst(array, i, mid - 1)
  right = _make_bst(array, mid + 1, j)
  return Node(left, right, array[mid])


def in_order(n):
  """Return the values of the tree via in-order traversal (sorted for a BST)."""
  if n is None:
    return []
  return in_order(n.left) + [n.value] + in_order(n.right)


def height(n):
  if n is None:
    return 0
  return max(height(n.left), height(n.right)) + 1


def is_bst(n, min_val=None, max_val=None):
  if n is None:
    return True
  if (min_val is not None and n.value <= min_val) or \
     (max_val is not None and n.value >= max_val):
    return False
  return is_bst(n.left, min_val, n.value) and is_bst(n.right, n.value, max_val)


class TestMakeBst(unittest.TestCase):
  def test_empty_array_returns_none(self):
    self.assertIsNone(make_bst([]))

  def test_single_element(self):
    root = make_bst([1])
    assert root is not None
    self.assertEqual(root.value, 1)
    self.assertIsNone(root.left)
    self.assertIsNone(root.right)

  def test_in_order_recovers_sorted_array(self):
    array = [1, 2, 3, 4, 5, 6, 7]
    self.assertEqual(in_order(make_bst(array)), array)

  def test_result_is_a_valid_bst(self):
    self.assertTrue(is_bst(make_bst([1, 2, 3, 4, 5, 6, 7])))

  def test_minimal_height_odd(self):
    # 7 elements: minimal height is ceil(log2(8)) = 3.
    self.assertEqual(height(make_bst([1, 2, 3, 4, 5, 6, 7])), 3)

  def test_minimal_height_even(self):
    # 4 elements: minimal height is 3.
    self.assertEqual(height(make_bst([1, 2, 3, 4])), 3)

  def test_two_elements(self):
    root = make_bst([1, 2])
    self.assertEqual(in_order(root), [1, 2])
    self.assertEqual(height(root), 2)


if __name__ == '__main__':
  unittest.main()
