# Binary Tree Vertical Order Traversal
#
# Source: https://www.careercup.com/question?id=5749533368647680
#
# You are given the root of a binary tree of integers. Assign the root column 0;
# a left child sits one column to the left of its parent and a right child one
# column to the right. Traverse the tree top-to-bottom, level by level.
#
# Return the vertical order traversal: a list of columns ordered from the
# leftmost column to the rightmost, where each column is the list of node values
# in that column read top-to-bottom. Nodes that share the same row and column
# appear in left-to-right (breadth-first) order.
#
# Constraints:
#   - 0 <= number of nodes <= 10^4
#   - node values are arbitrary integers
#
# Examples:
#           1
#         /   \
#        2     3            -> [[4], [2], [1, 5, 6], [3], [7]]
#       / \   / \
#      4   5 6   7          (5 and 6 both land in column 0 with the root)
#
#   root = None            -> []
#   single node 9         -> [[9]]
#   left chain 1 -> 2 -> 3 -> [[3], [2], [1]]


class TreeNode:
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right


def vertical_order(root):
  # TODO: implement
  raise NotImplementedError
