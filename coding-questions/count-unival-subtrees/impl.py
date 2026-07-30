# Count Unival Subtrees
#
# Difficulty: medium
# Tags: #tree #dfs #recursion #box
#
# You are given the root of a tree in which every node holds a value and a list
# of children (a node may have any number of children; a node with no children is
# a leaf). A subtree is "unival" (universal-value) if every node in that subtree
# holds the same value.
#
# Return the number of unival subtrees in the tree. The subtree rooted at a node
# is counted whenever all of its nodes share a single value; every leaf is
# trivially a unival subtree.
#
# Constraints:
#   - the tree may be empty (root is None), in which case the answer is 0
#   - node values may be any integers
#
# Examples:
#   root 1 with children [1, 1, 1]           -> 4  (3 leaves + the root)
#   root 1 with children [1, 1]              -> 3  (2 leaves + the root)
#   root 1, children [A, B] where A has value
#     1 and a single child of value 2, and B
#     is a leaf of value 1                   -> 2  (the value-2 leaf and B; A and
#                                                   the root are not unival)
#   an empty tree                            -> 0
#
# Approach: post-order DFS returning whether each subtree is unival; a node is
# unival iff every child subtree is unival and shares the node's value.


class Node:
  def __init__(self, value, children=None):
    self.value = value
    self.children = children if children is not None else []


def count_unival_subtrees(root):
  # TODO: implement
  raise NotImplementedError
