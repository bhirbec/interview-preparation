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


class Node(object):
  def __init__(self, left, right, value):
    self.left = left
    self.right = right
    self.value = value


def make_bst(array):
  # TODO: implement
  raise NotImplementedError
