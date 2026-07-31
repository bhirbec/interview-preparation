# Validate BST
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


class Node():
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right


def is_bst(n):
  # TODO: implement
  raise NotImplementedError
