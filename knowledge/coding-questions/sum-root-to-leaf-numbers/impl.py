# Sum Root To Leaf Numbers
#
# Difficulty: medium
# Tags: #tree #dfs #recursion #google
#
# You are given the root of a binary tree in which every node holds a single
# digit (0-9). Each root-to-leaf path spells out a number by concatenating the
# digits from the root down to the leaf. Return the sum of all such numbers.
#
# Constraints:
#   - Node values are single digits 0-9.
#   - A leaf is a node with no children.
#   - The tree may be empty (root is None), in which case the sum is 0.
#
# Examples:
#         1
#        / \
#       3   4
#      /   / \
#     7   2   3
#            / \
#           9   1
#     paths: 137 + 142 + 1439 + 1431 = 3149
#
#   Node(5) alone           -> 5
#   1 -> 2 -> 3 (left chain) -> 123
#   empty tree               -> 0
#
# Approach: DFS carrying the number built so far (current * 10 + node value);
# at each leaf add the accumulated number to the running total.


class Node(object):
  def __init__(self, value, left=None, right=None):
    self.value = value
    self.left = left
    self.right = right


def sum_root_to_leaf(root):
  # TODO: implement
  raise NotImplementedError
