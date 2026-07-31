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


def is_balanced(n):
  # TODO: implement
  raise NotImplementedError
